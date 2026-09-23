/* Shared microphone capture + VAD segmenter for voice commands (offline STT). */
(function (global) {
    'use strict';

    const TARGET_RATE = 16000;
    const MIN_SPEECH_MS = 250;
    const MIN_SEGMENT_SAMPLES = 1600;
    const MAX_SEGMENT_MS = 20000;

    function floatTo16kPCM(float32, srcRate) {
        const target = TARGET_RATE;
        if (srcRate === target) {
            const out = new Int16Array(float32.length);
            for (let i = 0; i < float32.length; i++) {
                const s = Math.max(-1, Math.min(1, float32[i]));
                out[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
            }
            return out;
        }
        const ratio = srcRate / target;
        const nOut = Math.max(1, Math.floor(float32.length / ratio));
        const out = new Int16Array(nOut);
        for (let i = 0; i < nOut; i++) {
            const idx = i * ratio;
            const i0 = Math.floor(idx);
            const i1 = Math.min(float32.length - 1, i0 + 1);
            const frac = idx - i0;
            const s = float32[i0] * (1 - frac) + float32[i1] * frac;
            const c = Math.max(-1, Math.min(1, s));
            out[i] = c < 0 ? c * 0x8000 : c * 0x7FFF;
        }
        return out;
    }

    function encodeWav(pcm16, sampleRate) {
        const buffer = new ArrayBuffer(44 + pcm16.length * 2);
        const view = new DataView(buffer);
        const writeStr = (off, s) => {
            for (let i = 0; i < s.length; i++) view.setUint8(off + i, s.charCodeAt(i));
        };
        writeStr(0, 'RIFF');
        view.setUint32(4, 36 + pcm16.length * 2, true);
        writeStr(8, 'WAVE');
        writeStr(12, 'fmt ');
        view.setUint32(16, 16, true);
        view.setUint16(20, 1, true);
        view.setUint16(22, 1, true);
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true);
        view.setUint16(32, 2, true);
        view.setUint16(34, 16, true);
        writeStr(36, 'data');
        view.setUint32(40, pcm16.length * 2, true);
        let off = 44;
        for (let i = 0; i < pcm16.length; i++, off += 2) view.setInt16(off, pcm16[i], true);
        return new Blob([view], { type: 'audio/wav' });
    }

    function rmsOf(data) {
        let sum = 0;
        for (let i = 0; i < data.length; i++) sum += data[i] * data[i];
        return Math.sqrt(sum / data.length);
    }

    /**
     * Voice session controller.
     * mode: 'manual' — buffer until stop() → one onSegment
     *       'vad'    — speech+pause → onSegment, keep listening until stop()
     */
    function createSession(opts) {
        const o = opts || {};
        const mode = o.mode === 'vad' ? 'vad' : 'manual';
        const vad = Object.assign({
            threshold: 0.018,
            silenceMs: 800,
            hangoverMs: 180,
            adaptNoise: true,
            noiseFloorMs: 400
        }, o.vad || {});

        let audioCtx = null;
        let mediaStream = null;
        let processor = null;
        let sourceNode = null;
        let running = false;
        let state = 'idle';
        let allChunks = [];
        let segChunks = [];
        let segStartAt = 0;
        let lastLoudAt = 0;
        let noiseFloor = vad.threshold;
        let noiseCalibMs = 0;
        let submitting = false;

        function emitState(info) {
            if (o.onState) o.onState(state, info || {});
        }

        function emitLevel(rms) {
            if (o.onLevel) o.onLevel(rms);
        }

        function thresholdNow() {
            if (!vad.adaptNoise) return vad.threshold;
            return Math.max(vad.threshold * 0.35, noiseFloor * 2.5, 0.012);
        }

        function clearSeg() {
            segChunks = [];
            segStartAt = 0;
            lastLoudAt = 0;
        }

        function merge(chunks) {
            let total = 0;
            for (let i = 0; i < chunks.length; i++) total += chunks[i].length;
            const merged = new Float32Array(total);
            let off = 0;
            for (let i = 0; i < chunks.length; i++) {
                merged.set(chunks[i], off);
                off += chunks[i].length;
            }
            return merged;
        }

        async function wavFrom(chunks) {
            if (!chunks.length) return null;
            const merged = merge(chunks);
            const durMs = (merged.length / (audioCtx ? audioCtx.sampleRate : 48000)) * 1000;
            if (durMs < MIN_SPEECH_MS) return null;
            const pcm = floatTo16kPCM(merged, audioCtx.sampleRate);
            if (pcm.length < MIN_SEGMENT_SAMPLES) return null;
            return encodeWav(pcm, TARGET_RATE);
        }

        async function flushVad(force) {
            if (!segChunks.length || submitting) return;
            const chunks = segChunks;
            clearSeg();
            const wav = await wavFrom(chunks);
            if (!wav) return;
            if (state !== 'idle') state = 'submitting';
            submitting = true;
            emitState({ reason: force ? 'force' : 'silence' });
            try {
                if (o.onSegment) await o.onSegment(wav);
            } catch (e) {
                if (o.onError) o.onError(e);
            } finally {
                submitting = false;
                if (running) {
                    state = 'listening';
                    emitState({});
                }
            }
        }

        function handleFrame(data, nowMs) {
            const rms = rmsOf(data);
            emitLevel(rms);

            if (mode === 'manual') {
                allChunks.push(new Float32Array(data));
                return;
            }

            if (vad.adaptNoise && noiseCalibMs < vad.noiseFloorMs && !segChunks.length && rms < thresholdNow() * 1.5) {
                noiseFloor = Math.min(0.05, noiseFloor * 0.9 + rms * 0.1);
                noiseCalibMs += (data.length / (audioCtx.sampleRate || 48000)) * 1000;
            }

            if (submitting) return;

            const loud = rms >= thresholdNow();

            if (!segChunks.length) {
                if (loud) {
                    segChunks.push(new Float32Array(data));
                    segStartAt = nowMs;
                    lastLoudAt = nowMs;
                    state = 'speaking';
                    emitState({ rms });
                } else {
                    state = 'listening';
                }
                return;
            }

            if (loud) {
                lastLoudAt = nowMs;
                segChunks.push(new Float32Array(data));
            } else {
                segChunks.push(new Float32Array(data));
            }

            const speechMs = nowMs - segStartAt;
            const quietMs = nowMs - lastLoudAt;
            const maxed = speechMs >= MAX_SEGMENT_MS;
            if (quietMs >= vad.silenceMs + vad.hangoverMs || maxed) {
                flushVad(maxed);
            }
        }

        async function start() {
            if (running) return;
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                const err = new Error('getUserMedia is not available in this browser.');
                if (o.onError) o.onError(err);
                throw err;
            }
            try {
                mediaStream = await navigator.mediaDevices.getUserMedia({
                    audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true }
                });
            } catch (e) {
                if (o.onError) o.onError(e);
                throw e;
            }
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            sourceNode = audioCtx.createMediaStreamSource(mediaStream);
            processor = audioCtx.createScriptProcessor(4096, 1, 1);
            allChunks = [];
            clearSeg();
            noiseFloor = vad.threshold;
            noiseCalibMs = 0;
            submitting = false;
            state = mode === 'vad' ? 'listening' : 'speaking';
            processor.onaudioprocess = (ev) => {
                if (!running) return;
                handleFrame(ev.inputBuffer.getChannelData(0), performance.now());
            };
            sourceNode.connect(processor);
            processor.connect(audioCtx.destination);
            running = true;
            emitState({});
        }

        async function stop(stopOpts) {
            const flush = !stopOpts || stopOpts.flush !== false;
            const wasRunning = running;
            running = false;
            if (wasRunning && flush && mode === 'manual' && allChunks.length) {
                const chunks = allChunks;
                allChunks = [];
                const wav = await wavFrom(chunks);
                if (wav && o.onSegment) {
                    try { await o.onSegment(wav); } catch (e) { if (o.onError) o.onError(e); }
                }
            } else if (wasRunning && flush && mode === 'vad' && segChunks.length) {
                await flushVad(true);
            }
            allChunks = [];
            clearSeg();
            try {
                if (processor) processor.disconnect();
                if (sourceNode) sourceNode.disconnect();
                if (mediaStream) mediaStream.getTracks().forEach(t => t.stop());
            } catch (e) { /* ignore */ }
            if (audioCtx && audioCtx.state !== 'closed') audioCtx.close().catch(() => {});
            audioCtx = null; processor = null; sourceNode = null; mediaStream = null;
            state = 'idle';
            emitState({});
        }

        return {
            mode,
            get running() { return running; },
            get state() { return state; },
            start,
            stop,
            setVad(patch) { Object.assign(vad, patch || {}); },
            getVad() { return Object.assign({}, vad); },
            floatTo16kPCM,
            encodeWav
        };
    }

    global.VoiceCore = {
        createSession,
        floatTo16kPCM,
        encodeWav,
        TARGET_RATE
    };
})(window);

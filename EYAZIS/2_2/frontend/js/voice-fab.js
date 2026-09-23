/* Global floating voice FAB: one-click continuous VAD voice commands. */
(function () {
    'use strict';
    if (window.__voiceFabInit) return;
    window.__voiceFabInit = true;

    const LANG_KEY = 'voice_lang';
    const NOTIFY_KEY = 'voice_notify';
    const DOC_KEY = 'voice_doc_id';

    let lang = localStorage.getItem(LANG_KEY) || 'en';
    if (lang !== 'en' && lang !== 'fr') lang = 'en';
    let notifyOn = localStorage.getItem(NOTIFY_KEY) !== '0';
    let docId = localStorage.getItem(DOC_KEY) || '';
    let session = null;
    let busy = false;
    let mutedUntil = 0;

    function el(id) { return document.getElementById(id); }

    function buildDom() {
        const wrap = document.createElement('div');
        wrap.className = 'voice-fab-root';
        wrap.innerHTML = `
            <div id="voiceFabPanel" class="voice-fab-panel hidden" role="dialog" aria-label="Voice settings">
                <div class="voice-fab-panel-title">Voice control</div>
                <label class="voice-fab-field">
                    <span>Recognition language</span>
                    <select id="voiceFabLang">
                        <option value="en">English (en)</option>
                        <option value="fr">Français (fr)</option>
                    </select>
                </label>
                <label class="voice-fab-field">
                    <span>Document (for summarize)</span>
                    <select id="voiceFabDoc"><option value="">— none —</option></select>
                </label>
                <label class="voice-fab-check">
                    <input type="checkbox" id="voiceFabNotify"> Voice notify (TTS)
                </label>
                <div id="voiceFabStatus" class="voice-fab-status">Idle — click mic to start</div>
            </div>
            <button id="voiceFabSettings" class="voice-fab-settings" title="Voice settings" aria-label="Voice settings">⚙</button>
            <button id="voiceFabBtn" class="voice-fab-btn" title="Voice command (click to start/stop)" aria-label="Voice command">
                <svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor" aria-hidden="true">
                    <path d="M12 14a3 3 0 0 0 3-3V5a3 3 0 1 0-6 0v6a3 3 0 0 0 3 3z"/>
                    <path d="M17 11a1 1 0 1 0-2 0 3 3 0 0 1-6 0 1 1 0 1 0-2 0 5 5 0 0 0 4 4.9V18a1 1 0 1 0 2 0v-2.1A5 5 0 0 0 17 11z"/>
                </svg>
            </button>
            <div id="voiceFabToasts" class="voice-toasts" aria-live="polite"></div>
        `;
        document.body.appendChild(wrap);
    }

    function setStatus(msg) {
        const s = el('voiceFabStatus');
        if (s) s.textContent = msg || '';
    }

    function toast(msg, kind) {
        const box = el('voiceFabToasts');
        if (!box) return;
        const div = document.createElement('div');
        div.className = 'voice-toast' + (kind === 'error' ? ' voice-toast-error' : '');
        div.textContent = msg;
        box.appendChild(div);
        setTimeout(() => {
            div.classList.add('voice-toast-out');
            setTimeout(() => div.remove(), 350);
        }, 4200);
    }

    function setBtnState(state) {
        const btn = el('voiceFabBtn');
        if (!btn) return;
        btn.classList.toggle('is-listening', state === 'listening' || state === 'speaking' || state === 'submitting');
        btn.classList.toggle('is-busy', state === 'submitting');
        btn.title = btn.classList.contains('is-listening')
            ? 'Listening — click to stop'
            : 'Voice command — click to start';
    }

    async function speakText(text) {
        if (!notifyOn || !text) return;
        mutedUntil = performance.now() + 4000;
        try {
            const res = await fetch('/api/tts/synthesize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, lang, rate: 1.0, volume: 100, pitch: 50 })
            });
            if (!res.ok) return;
            const blob = await res.blob();
            const audio = new Audio(URL.createObjectURL(blob));
            await new Promise((resolve) => {
                const done = () => {
                    mutedUntil = performance.now() + 400;
                    resolve();
                };
                audio.onended = done;
                audio.onerror = done;
                setTimeout(done, 15000);
                audio.play().catch(done);
            });
        } catch (e) { /* optional */ }
    }

    function applyClientAction(action) {
        if (!action) return;
        if (action.startsWith('navigate:')) {
            const page = action.slice('navigate:'.length);
            setTimeout(() => { window.location.href = page; }, 700);
        }
    }

    async function sendRecognize(wavBlob) {
        if (busy) return;
        busy = true;
        const fd = new FormData();
        fd.append('lang', lang);
        fd.append('wav', wavBlob, 'cmd.wav');
        if (docId) fd.append('doc_id', docId);
        setStatus('Recognizing…');
        try {
            const started = performance.now();
            const res = await fetch('/api/stt/recognize', { method: 'POST', body: fd });
            const data = await res.json();
            const ms = Math.round(performance.now() - started);
            if (data.error) {
                setStatus(data.error);
                toast(data.error, 'error');
                return;
            }
            const heard = data.text || '(silence)';
            setStatus(`Heard: “${heard}” → ${data.operation || 'no match'}`);
            const notifyMsg = data.notify ? (data.notify[lang] || data.notify.en) : '';
            const conf = data.matched ? Number(data.confidence).toFixed(2) : '—';
            toast(
                `${data.operation || 'no match'}${data.argument ? ' · ' + data.argument : ''} · conf ${conf} · “${heard}”`,
                data.matched ? '' : 'error'
            );
            window.dispatchEvent(new CustomEvent('voice-result', { detail: data }));
            if (notifyMsg) await speakText(notifyMsg);
            if (data.matched) {
                if (data.speak) await speakText(data.speak);
                applyClientAction(data.client_action);
            }
        } catch (e) {
            setStatus('Recognize failed: ' + e.message);
            toast('Recognize failed: ' + e.message, 'error');
        } finally {
            busy = false;
        }
    }

    async function loadDocs() {
        const sel = el('voiceFabDoc');
        if (!sel) return;
        try {
            const res = await fetch('/api/documents');
            const data = await res.json();
            const docs = data.documents || data.items || (Array.isArray(data) ? data : []);
            sel.innerHTML = '<option value="">— none —</option>';
            docs.forEach(d => {
                const opt = document.createElement('option');
                opt.value = String(d.id);
                opt.textContent = '#' + d.id + ' ' + (d.title || '').slice(0, 40);
                sel.appendChild(opt);
            });
            if (docId) sel.value = docId;
        } catch (e) { /* optional */ }
    }

    async function toggleSession() {
        if (session && session.running) {
            await session.stop();
            setStatus('Stopped.');
            setBtnState('idle');
            return;
        }
        if (!window.VoiceCore) {
            toast('voice-core.js not loaded', 'error');
            return;
        }
        // conflict: page-local mic (stt.js manual session) — let VoiceCore lock via our own flag
        if (window.__voiceLocalRecording) {
            toast('Stop the page Record button first', 'error');
            return;
        }
        session = VoiceCore.createSession({
            mode: 'vad',
            vad: { threshold: 0.018, silenceMs: 800, hangoverMs: 180 },
            onLevel(rms) {
                const meter = el('recLevel');
                if (meter && window.__voiceFabIsStt) {
                    meter.style.width = Math.min(100, Math.round(rms * 400)) + '%';
                }
            },
            onState(state) {
                setBtnState(state);
                if (state === 'listening') setStatus('Listening… say a command, pause to send.');
                else if (state === 'speaking') setStatus('Speech detected…');
                else if (state === 'submitting') setStatus('Recognizing…');
                else if (state === 'idle') setStatus('Stopped.');
            },
            onSegment(wav) {
                if (performance.now() < mutedUntil) return Promise.resolve();
                return sendRecognize(wav);
            },
            onError(err) {
                toast(err.message || String(err), 'error');
                setStatus(err.message || String(err));
            }
        });
        try {
            await session.start();
            setStatus('Listening… say a command, pause to send.');
            setBtnState('listening');
        } catch (e) { /* handled in onError */ }
    }

    function init() {
        if (!document.body) return;
        buildDom();
        const langSel = el('voiceFabLang');
        const docSel = el('voiceFabDoc');
        const notifyCb = el('voiceFabNotify');
        const btn = el('voiceFabBtn');
        const gear = el('voiceFabSettings');
        const panel = el('voiceFabPanel');

        langSel.value = lang;
        notifyCb.checked = notifyOn;
        loadDocs();

        langSel.addEventListener('change', () => {
            lang = langSel.value;
            localStorage.setItem(LANG_KEY, lang);
            window.dispatchEvent(new CustomEvent('voice-lang', { detail: { lang } }));
        });
        docSel.addEventListener('change', () => {
            docId = docSel.value;
            localStorage.setItem(DOC_KEY, docId);
        });
        notifyCb.addEventListener('change', () => {
            notifyOn = notifyCb.checked;
            localStorage.setItem(NOTIFY_KEY, notifyOn ? '1' : '0');
        });

        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleSession();
        });
        gear.addEventListener('click', (e) => {
            e.stopPropagation();
            panel.classList.toggle('hidden');
        });
        document.addEventListener('click', (e) => {
            if (!panel.classList.contains('hidden') &&
                !panel.contains(e.target) && e.target !== btn && !btn.contains(e.target) &&
                e.target !== gear && !gear.contains(e.target)) {
                panel.classList.add('hidden');
            }
        });

        // expose for stt.js sync
        window.VoiceFab = {
            get lang() { return lang; },
            set lang(v) {
                lang = v;
                localStorage.setItem(LANG_KEY, lang);
                if (langSel) langSel.value = lang;
            },
            get docId() { return docId; },
            set docId(v) {
                docId = v || '';
                localStorage.setItem(DOC_KEY, docId);
                if (docSel) docSel.value = docId;
            },
            get session() { return session; },
            stop: async () => { if (session && session.running) await session.stop(); },
            toast
        };
    }

    if (document.body) {
        init();
    } else if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

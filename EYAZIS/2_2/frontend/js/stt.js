const API = '';

const els = {
    lang: document.getElementById('langSelect'),
    doc: document.getElementById('docSelect'),
    micBtn: document.getElementById('micBtn'),
    saySample: document.getElementById('saySampleBtn'),
    status: document.getElementById('sttStatus'),
    chips: document.getElementById('sttChips'),
    log: document.getElementById('logBox'),
    lastResult: document.getElementById('lastResult'),
    op: document.getElementById('stOp'),
    conf: document.getElementById('stConf'),
    recMs: document.getElementById('stRecMs'),
    phrase: document.getElementById('stPhrase'),
    notify: document.getElementById('notifyBox'),
    heard: document.getElementById('heardBox'),
    voiceNotify: document.getElementById('voiceNotify'),
    editor: document.getElementById('commandsEditor'),
    saveCmd: document.getElementById('saveCmdBtn'),
    resetCmd: document.getElementById('resetCmdBtn'),
    cmdStatus: document.getElementById('cmdStatus'),
    level: document.getElementById('recLevel')
};

let commandsData = { operations: [], defaults: [] };
let manualSession = null;

function setStatus(msg, isError) {
    els.status.textContent = msg || '';
    els.status.style.color = isError ? '#dc2626' : '';
}

function setCmdStatus(msg, isError) {
    els.cmdStatus.textContent = msg || '';
    els.cmdStatus.style.color = isError ? '#dc2626' : '#16a34a';
}

function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
}

function addLog(html) {
    const empty = els.log.querySelector('span');
    if (empty && empty.textContent.includes('no commands')) els.log.innerHTML = '';
    const div = document.createElement('div');
    div.style.padding = '4px 0';
    div.style.borderBottom = '1px solid var(--border)';
    div.innerHTML = html;
    els.log.prepend(div);
}

async function loadStatus() {
    try {
        const res = await fetch(API + '/api/stt/status');
        const s = await res.json();
        const chips = [];
        const models = s.vosk && s.vosk.models ? s.vosk.models : {};
        const ok = Object.values(models).filter(Boolean).length;
        chips.push(`<span style="padding:4px 10px; border-radius:12px; border:1px solid var(--border); background:${s.vosk && s.vosk.available && ok ? '#dcfce7' : '#fee2e2'};">Vosk: ${ok} model(s) (en/fr)</span>`);
        chips.push(`<span style="padding:4px 10px; border-radius:12px; border:1px solid var(--border); background:#EAF2FB;">rate ${s.sample_rate || 16000} Hz, max ${s.max_audio_seconds || 30}s</span>`);
        if (s.commands) chips.push(`<span style="padding:4px 10px; border-radius:12px; border:1px solid var(--border); background:#EAF2FB;">${s.commands.operations} operations</span>`);
        els.chips.innerHTML = chips.join('');
    } catch (e) {
        els.chips.innerHTML = '<span style="color:#dc2626;">status unavailable</span>';
    }
}

async function loadDocuments() {
    try {
        const res = await fetch(API + '/api/documents');
        const data = await res.json();
        const docs = data.documents || data.items || (Array.isArray(data) ? data : []);
        docs.slice(0, 50).forEach(d => {
            const opt = document.createElement('option');
            opt.value = d.id;
            opt.textContent = (d.title || ('doc ' + d.id)).slice(0, 60);
            els.doc.appendChild(opt);
        });
    } catch (e) { /* documents optional */ }
}

function renderCommands() {
    const ops = commandsData.operations || [];
    els.editor.innerHTML = ops.map(op => {
        const en = (op.phrases && op.phrases.en || []).join('\n');
        const fr = (op.phrases && op.phrases.fr || []).join('\n');
        return `<div style="border:1px solid var(--border); border-radius:8px; padding:8px; margin-bottom:8px;" data-op="${escapeHtml(op.id)}">
            <div style="display:flex; justify-content:space-between; gap:8px; margin-bottom:6px;">
                <strong>${escapeHtml(op.id)}</strong>
                <span style="color:var(--text-light);">${escapeHtml(op.description || '')}</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                <div><label style="font-size:0.8rem;">EN phrases</label>
                    <textarea data-lang="en" rows="3" style="width:100%; font-size:0.82rem; padding:4px; border:1px solid var(--border); border-radius:4px;">${escapeHtml(en)}</textarea></div>
                <div><label style="font-size:0.8rem;">FR phrases</label>
                    <textarea data-lang="fr" rows="3" style="width:100%; font-size:0.82rem; padding:4px; border:1px solid var(--border); border-radius:4px;">${escapeHtml(fr)}</textarea></div>
            </div>
        </div>`;
    }).join('');
}

async function loadCommands() {
    try {
        const res = await fetch(API + '/api/stt/commands');
        const data = await res.json();
        if (data.error) { setCmdStatus(data.error, true); return; }
        commandsData = data;
        renderCommands();
    } catch (e) {
        setCmdStatus('Cannot load commands: ' + e.message, true);
    }
}

async function saveCommands() {
    const ops = [...els.editor.querySelectorAll('[data-op]')].map(box => {
        const id = box.getAttribute('data-op');
        const phrases = {};
        box.querySelectorAll('textarea').forEach(ta => {
            phrases[ta.getAttribute('data-lang')] = ta.value.split('\n').map(s => s.trim()).filter(Boolean);
        });
        return { id, phrases };
    });
    try {
        const res = await fetch(API + '/api/stt/commands', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ operations: ops })
        });
        const data = await res.json();
        if (data.error) { setCmdStatus(data.error, true); return; }
        commandsData.operations = data.operations;
        renderCommands();
        setCmdStatus('Saved.', false);
    } catch (e) {
        setCmdStatus('Save failed: ' + e.message, true);
    }
}

async function resetCommands() {
    try {
        const res = await fetch(API + '/api/stt/commands/reset', { method: 'POST' });
        const data = await res.json();
        if (data.error) { setCmdStatus(data.error, true); return; }
        commandsData.operations = data.operations;
        renderCommands();
        setCmdStatus('Defaults restored.', false);
    } catch (e) {
        setCmdStatus('Reset failed: ' + e.message, true);
    }
}

async function speakText(text) {
    if (!els.voiceNotify.checked || !text) return;
    try {
        const res = await fetch(API + '/api/tts/synthesize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text,
                lang: els.lang.value,
                rate: 1.0, volume: 100, pitch: 50
            })
        });
        if (!res.ok) return;
        const blob = await res.blob();
        const audio = new Audio(URL.createObjectURL(blob));
        await audio.play().catch(() => {});
    } catch (e) { /* notification voice is optional */ }
}

function applyClientAction(action) {
    if (!action) return;
    if (action.startsWith('navigate:')) {
        const page = action.slice('navigate:'.length);
        setTimeout(() => { window.location.href = page; }, 600);
    }
}

async function sendRecognize(wavBlob) {
    const lang = els.lang.value;
    const fd = new FormData();
    fd.append('lang', lang);
    fd.append('wav', wavBlob, 'cmd.wav');
    if (els.doc.value) fd.append('doc_id', els.doc.value);

    setStatus('Recognizing…');
    try {
        const started = performance.now();
        const res = await fetch(API + '/api/stt/recognize', { method: 'POST', body: fd });
        const data = await res.json();
        if (data.error) { setStatus(data.error, true); return; }

        const clientMs = Math.round(performance.now() - started);
        els.heard.textContent = data.text
            ? `Heard: “${data.text}”`
            : 'Heard: (silence / nothing)';
        els.lastResult.style.display = 'flex';
        els.op.textContent = data.operation || (data.matched ? '?' : 'none');
        els.conf.textContent = data.matched ? Number(data.confidence).toFixed(2) : '—';
        els.recMs.textContent = data.recognized_ms || clientMs;
        els.phrase.textContent = data.matched_phrase || '—';
        els.phrase.title = data.matched_phrase || '';

        if (data.notify) {
            els.notify.style.display = 'block';
            els.notify.textContent = data.notify[lang] || data.notify.en;
            await speakText(data.notify[lang] || data.notify.en);
        } else {
            els.notify.style.display = 'none';
        }

        const conf = data.matched ? Number(data.confidence).toFixed(2) : '—';
        addLog(`<strong>${escapeHtml(data.operation || 'no match')}</strong>
            ${data.argument ? '· <em>' + escapeHtml(data.argument) + '</em>' : ''}
            · conf ${conf} · ${escapeHtml(data.text || '∅')} · ${clientMs} ms`);

        if (data.matched) {
            setStatus('Done: ' + data.operation);
            if (data.speak) await speakText(data.speak);
            applyClientAction(data.client_action);
        } else {
            setStatus('Command not recognized.', true);
        }
    } catch (e) {
        setStatus('Recognize failed: ' + e.message, true);
    }
}

function renderRecognizeResult(data, clientMs) {
    const lang = els.lang.value;
    els.heard.textContent = data.text
        ? `Heard: “${data.text}”`
        : 'Heard: (silence / nothing)';
    els.lastResult.style.display = 'flex';
    els.op.textContent = data.operation || (data.matched ? '?' : 'none');
    els.conf.textContent = data.matched ? Number(data.confidence).toFixed(2) : '—';
    els.recMs.textContent = data.recognized_ms || clientMs;
    els.phrase.textContent = data.matched_phrase || '—';
    els.phrase.title = data.matched_phrase || '';

    if (data.notify) {
        els.notify.style.display = 'block';
        els.notify.textContent = data.notify[lang] || data.notify.en;
    } else {
        els.notify.style.display = 'none';
    }

    const conf = data.matched ? Number(data.confidence).toFixed(2) : '—';
    addLog(`<strong>${escapeHtml(data.operation || 'no match')}</strong>
        ${data.argument ? '· <em>' + escapeHtml(data.argument) + '</em>' : ''}
        · conf ${conf} · ${escapeHtml(data.text || '∅')} · ${clientMs} ms`);

    if (data.matched) setStatus('Done: ' + data.operation);
    else setStatus('Command not recognized.', true);
}

async function sendSamplePhrase() {
    setStatus('Press Record and say: “' + els.saySample.textContent.replace('Say: ', '') + '”.', false);
}

async function startRecording() {
    if (!window.VoiceCore) { setStatus('voice-core.js not loaded.', true); return; }
    if (window.VoiceFab && VoiceFab.session && VoiceFab.session.running) {
        setStatus('Stop the floating voice button first.', true);
        return;
    }
    manualSession = VoiceCore.createSession({
        mode: 'manual',
        onLevel(rms) {
            if (els.level) els.level.style.width = Math.min(100, Math.round(rms * 400)) + '%';
        },
        onState(state) {
            if (state === 'speaking') {
                els.micBtn.textContent = '■ Stop & Recognize';
                els.micBtn.classList.remove('btn-primary');
                els.micBtn.classList.add('btn-secondary');
                setStatus('Recording… speak a command, then press Stop.');
            } else if (state === 'idle') {
                els.micBtn.textContent = '● Record';
                els.micBtn.classList.add('btn-primary');
                els.micBtn.classList.remove('btn-secondary');
                if (els.level) els.level.style.width = '0%';
            }
        },
        onSegment(wav) { return sendRecognize(wav); },
        onError(err) { setStatus(err.message || String(err), true); }
    });
    window.__voiceLocalRecording = true;
    try {
        await manualSession.start();
    } catch (e) {
        window.__voiceLocalRecording = false;
        manualSession = null;
    }
}

async function stopRecording() {
    const s = manualSession;
    manualSession = null;
    window.__voiceLocalRecording = false;
    if (s) await s.stop();
}

async function handleVoiceFabResult(data) {
    const clientMs = data.recognized_ms || 0;
    renderRecognizeResult(data, clientMs);
    // TTS + client_action are handled by voice-fab.js — avoid double speak/nav
}

// sync language page <-> FAB
els.lang.addEventListener('change', () => {
    setStatus('Language: ' + els.lang.value.toUpperCase());
    if (window.VoiceFab) VoiceFab.lang = els.lang.value;
});
els.doc.addEventListener('change', () => {
    if (window.VoiceFab) VoiceFab.docId = els.doc.value;
});
els.voiceNotify.addEventListener('change', () => {
    try { localStorage.setItem('voice_notify', els.voiceNotify.checked ? '1' : '0'); } catch (e) {}
});

function adoptVoiceFabPrefs() {
    if (!window.VoiceFab) {
        setTimeout(adoptVoiceFabPrefs, 50);
        return;
    }
    if (VoiceFab.lang) els.lang.value = VoiceFab.lang;
    try {
        const stored = localStorage.getItem('voice_notify');
        if (stored !== null) els.voiceNotify.checked = stored === '1';
    } catch (e) {}
    const applyDoc = () => {
        if (VoiceFab.docId && [...els.doc.options].some(o => o.value === VoiceFab.docId)) {
            els.doc.value = VoiceFab.docId;
        }
    };
    applyDoc();
    // docs may still be loading
    let tries = 0;
    const waitDoc = () => {
        if (VoiceFab.docId && els.doc.options.length > 1) { applyDoc(); return; }
        if (++tries < 30) setTimeout(waitDoc, 100);
    };
    waitDoc();
}
adoptVoiceFabPrefs();

window.addEventListener('voice-result', (e) => {
    handleVoiceFabResult(e.detail);
});

window.addEventListener('voice-lang', (e) => {
    if (els.lang && e.detail && e.detail.lang) els.lang.value = e.detail.lang;
});

els.micBtn.addEventListener('click', async () => {
    if (manualSession && manualSession.running) await stopRecording();
    else await startRecording();
});

els.saySample.addEventListener('click', sendSamplePhrase);
els.saveCmd.addEventListener('click', saveCommands);
els.resetCmd.addEventListener('click', resetCommands);

// deep-link: stt.html?panel=commands
if (location.search.includes('panel=commands')) {
    setTimeout(() => document.getElementById('commandsPanel').scrollIntoView({ behavior: 'smooth' }), 300);
}

document.body.classList.add('voice-fab-is-stt');
window.__voiceFabIsStt = true;

loadStatus();
loadCommands();
loadDocuments();

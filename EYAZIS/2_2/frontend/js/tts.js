const API = '';

const SAMPLES = {
    fr1: '« Qui êtes-vous ? demanda le guichetier. — Je suis celui qui ne résiste jamais. » Cette réponse fit rire l\'huissier et ma femme, qui me trouvait ce jour-là d\'un abominable sérieux.',
    fr2: 'Ô temps, suspends ton vol, et vous, heures propices ; suspendez votre cours : laissez-nous savourer les rapides empreintes de nos jours, qui passent si vite.',
    en1: 'The artist is the creator of beautiful things. To reveal art and conceal the artist is art\'s aim. The critic is he who can learn about the art of the artist.',
    en2: 'Shall I compare thee to a summer\'s day? Thou art more lovely and more temperate: rough winds do shake the darling buds of May, and summer\'s lease hath all too short a date.'
};

const els = {
    text: document.getElementById('ttsText'),
    voice: document.getElementById('voiceSelect'),
    sample: document.getElementById('sampleSelect'),
    rate: document.getElementById('rateRange'),
    rateVal: document.getElementById('rateVal'),
    volume: document.getElementById('volumeRange'),
    volumeVal: document.getElementById('volumeVal'),
    pitch: document.getElementById('pitchRange'),
    pitchVal: document.getElementById('pitchVal'),
    btn: document.getElementById('synthBtn'),
    pasteBtn: document.getElementById('pasteBtn'),
    detectBtn: document.getElementById('detectBtn'),
    status: document.getElementById('ttsStatus'),
    player: document.getElementById('player'),
    stats: document.getElementById('ttsStats'),
    engineChips: document.getElementById('engineChips'),
    voiceInfo: document.getElementById('ttsVoiceInfo'),
    normalized: document.getElementById('ttsNormalized')
};

let voicesData = { voices: [], default_by_lang: {} };

function setStatus(msg, isError) {
    els.status.textContent = msg || '';
    els.status.style.color = isError ? '#dc2626' : '';
}

function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
}

function currentVoice() {
    return voicesData.voices.find(v => v.id === els.voice.value) || null;
}

function updatePitchEnabled() {
    const v = currentVoice();
    const isEspeak = v && v.engine === 'espeak';
    els.pitch.disabled = !isEspeak;
    els.pitch.parentElement.style.opacity = isEspeak ? '1' : '0.55';
}

function fillVoices(preferredLang) {
    const prev = els.voice.value;
    els.voice.innerHTML = '';
    const groups = { fr: 'French', en: 'English' };
    ['fr', 'en'].forEach(lang => {
        const list = voicesData.voices.filter(v => v.lang === lang);
        if (!list.length) return;
        const og = document.createElement('optgroup');
        og.label = groups[lang];
        list.forEach(v => {
            const opt = document.createElement('option');
            opt.value = v.id;
            opt.textContent = `${v.name} [${v.engine}]${v.available ? '' : ' — unavailable'}`;
            opt.disabled = !v.available;
            og.appendChild(opt);
        });
        els.voice.appendChild(og);
    });
    // restore selection or pick default for preferred lang
    const ids = voicesData.voices.filter(v => v.available).map(v => v.id);
    if (prev && ids.includes(prev)) {
        els.voice.value = prev;
    } else if (preferredLang && voicesData.default_by_lang[preferredLang] &&
               ids.includes(voicesData.default_by_lang[preferredLang])) {
        els.voice.value = voicesData.default_by_lang[preferredLang];
    } else if (ids.length) {
        els.voice.value = ids[0];
    }
    updatePitchEnabled();
}

async function loadVoices() {
    try {
        const res = await fetch(API + '/api/tts/voices');
        const data = await res.json();
        if (data.error) { setStatus(data.error, true); return; }
        voicesData = data;
        fillVoices(null);
    } catch (e) {
        setStatus('Cannot load voices: ' + e.message, true);
    }
}

async function loadStatus() {
    try {
        const res = await fetch(API + '/api/tts/status');
        const s = await res.json();
        const chips = [];
        const modelsOk = s.piper.models ? Object.values(s.piper.models).filter(Boolean).length : 0;
        chips.push(`<span style="padding:4px 10px; border-radius:12px; border:1px solid var(--border); background:${s.piper.available && modelsOk ? '#dcfce7' : '#fee2e2'};">Piper neural: ${modelsOk} model(s)</span>`);
        chips.push(`<span style="padding:4px 10px; border-radius:12px; border:1px solid var(--border); background:${s.espeak.available ? '#dcfce7' : '#fee2e2'};">eSpeak-NG: ${s.espeak.available ? 'ready' : 'missing'}</span>`);
        els.engineChips.innerHTML = chips.join('');
    } catch (e) {
        els.engineChips.innerHTML = '<span style="color:#dc2626;">status unavailable</span>';
    }
}

els.rate.addEventListener('input', () => { els.rateVal.textContent = Number(els.rate.value).toFixed(1) + '×'; });
els.volume.addEventListener('input', () => { els.volumeVal.textContent = els.volume.value + '%'; });
els.pitch.addEventListener('input', () => { els.pitchVal.textContent = els.pitch.value; });
els.voice.addEventListener('change', updatePitchEnabled);

els.sample.addEventListener('change', () => {
    const key = els.sample.value;
    if (key && SAMPLES[key]) els.text.value = SAMPLES[key];
});

els.pasteBtn.addEventListener('click', async () => {
    try {
        const clip = await navigator.clipboard.readText();
        if (clip) {
            els.text.value = clip;
            setStatus('Pasted from clipboard.');
        }
    } catch (e) {
        setStatus('Clipboard access denied — press Ctrl+V in the text field instead.', true);
    }
});

els.detectBtn.addEventListener('click', async () => {
    const text = els.text.value.trim();
    if (!text) { setStatus('Enter text first.', true); return; }
    setStatus('Detecting language...');
    try {
        const res = await fetch(API + '/api/tts/detect-lang', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text})
        });
        const data = await res.json();
        if (data.error) { setStatus(data.error, true); return; }
        const preferred = data.default_voice;
        fillVoices(data.lang);
        if (preferred && [...els.voice.options].some(o => o.value === preferred && !o.disabled)) {
            els.voice.value = preferred;
        }
        updatePitchEnabled();
        setStatus(`Detected: ${data.lang.toUpperCase()}${data.agreed ? ' (methods agree)' : ''} → voice ${els.voice.value}`);
    } catch (e) {
        setStatus('Detect failed: ' + e.message, true);
    }
});

els.btn.addEventListener('click', async () => {
    const text = els.text.value.trim();
    if (!text) { setStatus('Enter text first.', true); return; }

    els.btn.disabled = true;
    els.btn.textContent = 'Synthesizing...';
    setStatus('');

    const payload = {
        text,
        voice: els.voice.value,
        rate: Number(els.rate.value),
        volume: parseInt(els.volume.value, 10),
        pitch: parseInt(els.pitch.value, 10)
    };

    try {
        const started = performance.now();
        const res = await fetch(API + '/api/tts/synthesize', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        if (!res.ok) {
            let msg = 'HTTP ' + res.status;
            try { const err = await res.json(); if (err.error) msg = err.error; } catch (e) {}
            setStatus(msg, true);
            return;
        }
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        if (els.player.src) URL.revokeObjectURL(els.player.src);
        els.player.src = url;
        await els.player.play().catch(() => {});

        const clientMs = Math.round(performance.now() - started);
        els.stats.style.display = 'flex';
        document.getElementById('stVoice').textContent = res.headers.get('X-TTS-Voice') || '—';
        document.getElementById('stEngine').textContent = res.headers.get('X-TTS-Engine') || '—';
        document.getElementById('stElapsed').textContent = res.headers.get('X-TTS-Elapsed-Ms') || clientMs;
        document.getElementById('stDuration').textContent = res.headers.get('X-TTS-Duration-S') || '—';
        document.getElementById('stChars').textContent = res.headers.get('X-TTS-Chars') || text.length;

        const v = currentVoice();
        els.voiceInfo.textContent = v
            ? `${v.name} — lang ${v.lang.toUpperCase()}, gender ${v.gender}, engine ${v.engine}, model ${v.model}`
            : '';
        els.normalized.textContent = res.headers.get('X-TTS-Normalized') || text;
        setStatus('Done.');
    } catch (e) {
        setStatus('Synthesis failed: ' + e.message, true);
    } finally {
        els.btn.disabled = false;
        els.btn.textContent = 'Synthesize & Play';
    }
});

loadVoices();
loadStatus();

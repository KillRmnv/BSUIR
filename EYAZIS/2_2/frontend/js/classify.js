const API_BASE = '/api';

const modelStatus = document.getElementById('modelStatus');
const modelMeta = document.getElementById('modelMeta');
const trainBtn = document.getElementById('trainBtn');
const singleForm = document.getElementById('singleForm');
const langFileInput = document.getElementById('langFileInput');
const langFileName = document.getElementById('langFileName');
const langTextInput = document.getElementById('langTextInput');
const singleResult = document.getElementById('singleResult');
const batchBtn = document.getElementById('batchBtn');
const csvBtn = document.getElementById('csvBtn');
const printBtn = document.getElementById('printBtn');
const batchResults = document.getElementById('batchResults');
const classifyStatus = document.getElementById('classifyStatus');

let lastBatch = null;

const LANG_NAME = { en: 'English', fr: 'French' };
const METHOD_NAME = { ngram: 'N-grams', alphabet: 'Alphabet', neural: 'Neural' };

langFileInput.addEventListener('change', () => {
    langFileName.textContent = langFileInput.files.length > 0
        ? langFileInput.files[0].name
        : 'No file chosen';
});

function langBadge(lang) {
    if (!lang) return '<span class="lang-badge">—</span>';
    return `<span class="lang-badge lang-${escapeHtml(lang)}">${escapeHtml(LANG_NAME[lang] || lang)} (${escapeHtml(lang)})</span>`;
}

async function loadStatus() {
    try {
        const res = await fetch(`${API_BASE}/lang/status`);
        const data = await res.json();
        const methods = data.methods || {};
        const rows = ['ngram', 'alphabet', 'neural'].map(m => {
            const t = (methods[m] || {}).trained;
            return `${METHOD_NAME[m]}: ${t ? 'trained' : 'not trained'}`;
        });
        modelStatus.innerHTML = rows.map(r => `<span class="lang-badge">${escapeHtml(r)}</span>`).join(' ');
        const meta = data.metadata;
        if (meta) {
            modelMeta.classList.remove('hidden');
            modelMeta.textContent =
                `Neural: EN chunks=${meta.n_en_chunks}, FR chunks=${meta.n_fr_chunks}; ` +
                `train=${meta.train_accuracy}, holdout=${meta.holdout_accuracy}, ` +
                `${meta.train_seconds}s`;
        } else {
            modelMeta.classList.add('hidden');
        }
    } catch (err) {
        modelStatus.textContent = 'Server unavailable: ' + err.message;
    }
}

trainBtn.addEventListener('click', async () => {
    showStatus('Training models…', 'success');
    try {
        const res = await fetch(`${API_BASE}/lang/train`, { method: 'POST' });
        const data = await res.json();
        if (data.error) {
            showStatus(data.error, 'error');
        } else {
            showStatus('Models trained (N-grams + alphabet + neural).', 'success');
            await loadStatus();
        }
    } catch (err) {
        showStatus('Error: ' + err.message, 'error');
    }
});

singleForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    let res;
    try {
        if (langFileInput.files.length > 0) {
            const formData = new FormData();
            formData.append('file', langFileInput.files[0]);
            res = await fetch(`${API_BASE}/lang/classify`, { method: 'POST', body: formData });
        } else if (langTextInput.value.trim()) {
            res = await fetch(`${API_BASE}/lang/classify`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: langTextInput.value }),
            });
        } else {
            showStatus('Select a file or paste text.', 'error');
            return;
        }
        const data = await res.json();
        if (data.error) {
            showStatus(data.error, 'error');
            return;
        }
        renderSingle(data);
    } catch (err) {
        showStatus('Error: ' + err.message, 'error');
    }
});

function methodBlock(title, inner) {
    return `<div class="method-block"><div class="method-title">${title}</div>${inner}</div>`;
}

function renderSingle(data) {
    const m = data.methods || {};
    const agreed = data.agreed ? 'methods agreed' : 'methods DISAGREED';
    let html = `<div>Result (vote): ${langBadge(data.lang)} <span class="hint">${escapeHtml(agreed)}</span></div>`;

    if (m.ngram) {
        html += methodBlock('N-grams (out-of-place)',
            `<div>${langBadge(m.ngram.lang)}</div>
             <div class="hint">dist EN=${m.ngram.dist_en}, FR=${m.ngram.dist_fr}, margin=${m.ngram.margin}, ${m.ngram.elapsed_ms} ms</div>`);
    }
    if (m.alphabet) {
        html += methodBlock('Alphabet',
            `<div>${langBadge(m.alphabet.lang)}</div>
             <div class="hint">fr_ratio=${m.alphabet.fr_ratio}, FR/EN markers=${m.alphabet.fr_marker_hits}/${m.alphabet.en_marker_hits}, score=${m.alphabet.fr_score} (threshold ${m.alphabet.threshold}), ${m.alphabet.elapsed_ms} ms</div>`);
    }
    if (m.neural) {
        const lowCorpus = m.neural.metadata && m.neural.metadata.n_samples < 100;
        html += methodBlock('Neural (LogReg)',
            `<div>${langBadge(m.neural.lang)}</div>
             <div class="proba-row"><span>P(EN) = ${m.neural.proba_en}</span>
             <div class="proba-bar"><div class="proba-fill" style="width:${(m.neural.proba_en * 100).toFixed(1)}%"></div></div></div>
             <div class="proba-row"><span>P(FR) = ${m.neural.proba_fr}</span>
             <div class="proba-bar"><div class="proba-fill" style="width:${(m.neural.proba_fr * 100).toFixed(1)}%"></div></div></div>
             ${lowCorpus ? '<div style="color:#f59e0b;font-size:0.85em;margin-top:4px;">⚠ Low training corpus (' + m.neural.metadata.n_samples + ' samples). Confidence may be unreliable. Expand lang_seeds.py and retrain.</div>' : ''}
             <div class="hint">Time: ${m.neural.elapsed_ms} ms</div>`);
    } else {
        html += methodBlock('Neural (LogReg)', `<div class="hint">Not trained (scikit-learn required)</div>`);
    }
    html += `<div class="hint">Total: ${data.elapsed_ms} ms${data.chars !== undefined ? `, chars: ${data.chars}` : ''}</div>`;
    singleResult.classList.remove('empty-state');
    singleResult.innerHTML = html;
}

batchBtn.addEventListener('click', async () => {
    showStatus('Classifying corpus…', 'success');
    try {
        const res = await fetch(`${API_BASE}/lang/classify-batch`, { method: 'POST' });
        const data = await res.json();
        if (data.error) {
            showStatus(data.error, 'error');
            return;
        }
        lastBatch = data;
        renderBatch(data);
        classifyStatus.classList.add('hidden');
    } catch (err) {
        showStatus('Error: ' + err.message, 'error');
    }
});

function renderBatch(data) {
    batchResults.classList.remove('hidden');
    csvBtn.classList.remove('hidden');
    printBtn.classList.remove('hidden');
    const s = data.summary || {};
    document.getElementById('batchAccuracy').textContent = s.accuracy !== undefined ? s.accuracy.toFixed(3) : '-';
    document.getElementById('batchCorrect').textContent = s.correct !== undefined ? `${s.correct}/${s.total}` : '-';
    document.getElementById('batchTime').textContent = s.avg_time_ms !== undefined ? s.avg_time_ms : '-';

    const pm = s.per_method || {};
    document.getElementById('pmRow').innerHTML = ['ngram', 'alphabet', 'neural'].map(k => {
        const v = pm[k];
        const txt = v && v.trained
            ? `${METHOD_NAME[k]}: acc=${v.accuracy}, ${v.avg_time_ms} ms`
            : `${METHOD_NAME[k]}: not trained`;
        return `<div class="hint">${escapeHtml(txt)}</div>`;
    }).join('');

    const tbody = document.getElementById('batchTableBody');
    tbody.innerHTML = '';
    (data.documents || []).forEach(d => {
        const tr = document.createElement('tr');
        tr.className = d.correct ? 'row-ok' : 'row-miss';
        const dm = d.methods || {};
        const cell = (k) => {
            const v = dm[k];
            return v ? escapeHtml(v.lang) : '—';
        };
        tr.innerHTML = `
            <td>${escapeHtml(d.title || '')}</td>
            <td>${escapeHtml(d.true_lang || '?')}</td>
            <td>${langBadge(d.lang)}</td>
            <td>${cell('ngram')}</td>
            <td>${cell('alphabet')}</td>
            <td>${cell('neural')}</td>
            <td>${d.elapsed_ms !== undefined ? d.elapsed_ms : '-'}</td>
            <td>${d.correct ? '✓' : (d.error ? 'ERR' : '✗')}</td>
        `;
        tbody.appendChild(tr);
    });
}

csvBtn.addEventListener('click', () => {
    if (!lastBatch) return;
    const rows = [['filename', 'true_lang', 'vote', 'pred_ngram', 'pred_alphabet', 'pred_neural', 'correct', 'elapsed_ms']];
    (lastBatch.documents || []).forEach(d => {
        const dm = d.methods || {};
        const cell = (k) => (dm[k] ? dm[k].lang : '');
        rows.push([d.title || '', d.true_lang || '', d.lang || '',
            cell('ngram'), cell('alphabet'), cell('neural'),
            d.correct ? 1 : 0, d.elapsed_ms !== undefined ? d.elapsed_ms : '']);
    });
    const s = lastBatch.summary || {};
    rows.push([]);
    rows.push(['vote_accuracy', s.accuracy !== undefined ? s.accuracy : '']);
    rows.push(['vote_avg_time_ms', s.avg_time_ms !== undefined ? s.avg_time_ms : '']);
    if (s.confusion) rows.push(['vote_confusion', JSON.stringify(s.confusion)]);
    const pm = s.per_method || {};
    ['ngram', 'alphabet', 'neural'].forEach(k => {
        const v = pm[k];
        rows.push([k + '_accuracy', v && v.trained ? v.accuracy : 'not_trained']);
        if (v && v.trained) {
            rows.push([k + '_avg_ms', v.avg_time_ms]);
            rows.push([k + '_confusion', JSON.stringify(v.confusion)]);
        }
    });
    const csv = rows.map(r => r.map(csvCell).join(',')).join('\n');
    const blob = new Blob(["\uFEFF" + csv], { type: 'text/csv;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'lang_classification_report.csv';
    a.click();
    URL.revokeObjectURL(a.href);
});

function csvCell(v) {
    const s = String(v);
    return /[",\n;]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

function showStatus(message, type) {
    classifyStatus.textContent = message;
    classifyStatus.className = `upload-status ${type}`;
    classifyStatus.classList.remove('hidden');
    setTimeout(() => {
        classifyStatus.classList.add('hidden');
    }, 5000);
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

loadStatus();

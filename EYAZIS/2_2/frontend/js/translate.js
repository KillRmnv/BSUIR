const API = '';
let currentMode = 'dict';

// --- Tab switching ---
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-panel').forEach(p => { p.style.display = 'none'; p.classList.remove('active'); });
        tab.classList.add('active');
        const panel = document.getElementById('tab-' + tab.dataset.tab);
        if (panel) { panel.style.display = ''; panel.classList.add('active'); }
    });
});

// --- Mode toggle ---
function setMode(mode) {
    currentMode = mode;
    document.querySelectorAll('.mode-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.mode === mode);
    });
}

// ==================== WORD LIST TAB ====================

document.getElementById('tlBtn').addEventListener('click', async () => {
    const text = document.getElementById('tlText').value.trim();
    if (!text) return;

    const btn = document.getElementById('tlBtn');
    btn.textContent = 'Translating...';
    btn.disabled = true;

    try {
        const url = currentMode === 'nmt' ? API + '/api/translate-nmt' : API + '/api/translate';
        const res = await fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text})
        });
        const data = await res.json();
        if (data.error) { alert(data.error); return; }

        document.getElementById('tlResults').style.display = '';
        document.getElementById('tlTranslated').innerHTML = '<strong>French:</strong> ' + escapeHtml(data.translated_text);

        if (currentMode === 'dict') {
            document.getElementById('tlStats').style.display = '';
            document.getElementById('tlWordCount').textContent = data.stats.total_words;
            document.getElementById('tlTranslatedCount').textContent = data.stats.translated;
            document.getElementById('tlCoverage').textContent = data.stats.coverage + '%';
            document.getElementById('tlTable').style.display = '';
            renderSummary(data);
            renderDictTable(data.words);
        } else {
            document.getElementById('tlStats').style.display = '';
            document.getElementById('tlWordCount').textContent = data.word_count;
            document.getElementById('tlTranslatedCount').textContent = '—';
            document.getElementById('tlCoverage').textContent = 'NMT';
            document.getElementById('tlTable').style.display = 'none';
            document.getElementById('tlSummary').style.display = 'none';
        }

        document.getElementById('tlExportBtn').style.display = '';
        window._lastTlText = text;
    } catch (e) {
        alert('Error: ' + e.message);
    } finally {
        btn.textContent = 'Translate';
        btn.disabled = false;
    }
});

function renderDictTable(words) {
    const tbody = document.getElementById('tlBody');
    tbody.innerHTML = '';
    words.forEach((w, i) => {
        const tr = document.createElement('tr');
        tr.style.borderBottom = '1px solid var(--border)';
        tr.innerHTML = `
            <td style="padding:6px;">${i + 1}</td>
            <td style="padding:6px; font-weight:500;">${escapeHtml(w.en)}</td>
            <td style="padding:6px; color:var(--primary);">${escapeHtml(w.fr)}</td>
            <td style="padding:6px; font-size:0.85rem;">${escapeHtml(w.pos_en)} <span style="color:var(--text-secondary);">(${escapeHtml(w.pos_en_desc)})</span></td>
            <td style="padding:6px;">${w.translated ? '<span style="color:var(--success);">&#10004;</span>' : '<span style="color:var(--text-secondary);">&#8212;</span>'}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderSummary(data) {
    const el = document.getElementById('tlSummary');
    const s = data.stats;
    el.style.display = '';
    el.innerHTML = `
        <div class="summary-highlight" style="margin-top:1rem;">
            <div style="display:flex; gap:1.5rem; flex-wrap:wrap;">
                <div class="stat-item">
                    <span class="stat-value">${s.total_words}</span>
                    <span class="stat-label">Total words</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">${s.translated}</span>
                    <span class="stat-label">Translated</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">${s.coverage}%</span>
                    <span class="stat-label">Coverage</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">${s.processing_time}s</span>
                    <span class="stat-label">Time</span>
                </div>
            </div>
        </div>
    `;
}

// ==================== SYNTAX TREE TAB ====================

document.getElementById('parseBtn').addEventListener('click', async () => {
    const text = document.getElementById('parseText').value.trim();
    const lang = document.getElementById('parseLang').value;
    if (!text) return;

    const btn = document.getElementById('parseBtn');
    btn.textContent = 'Parsing...';
    btn.disabled = true;

    try {
        const res = await fetch(API + '/api/translate/parse', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text, lang})
        });
        const data = await res.json();
        if (data.error) { alert(data.error); return; }

        const container = document.getElementById('parseTrees');
        container.innerHTML = '';
        document.getElementById('parseResults').style.display = '';

        if (!data.results || data.results.length === 0) {
            container.innerHTML = '<p style="color:var(--text-secondary);">No parse results.</p>';
            return;
        }

        data.results.forEach((r, i) => {
            const card = document.createElement('div');
            card.style.cssText = 'border:1px solid var(--border); border-radius:8px; overflow:hidden; margin-bottom:1rem;';

            const header = document.createElement('button');
            header.style.cssText = 'width:100%; padding:1rem; background:var(--surface-hover, rgba(255,255,255,0.04)); border:none; display:flex; align-items:center; gap:12px; cursor:pointer; text-align:left; color:var(--text); font-size:0.95rem;';
            header.innerHTML = `
                <span style="flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                    <span style="color:var(--text-secondary);">Sentence ${i + 1}:</span> ${escapeHtml(r.sentence)}
                </span>
            `;

            const body = document.createElement('div');
            body.className = 'syntax-tree-body';
            body.style.cssText = 'display:none; padding:1.5rem; background:var(--bg, #1a1a24);';

            let expanded = false;
            header.addEventListener('click', () => {
                expanded = !expanded;
                body.style.display = expanded ? '' : 'none';
                header.querySelector('span').style.fontWeight = expanded ? '500' : '';
            });

            if (r.constituency_tree) {
                const scrollWrap = document.createElement('div');
                scrollWrap.className = 'constituency-tree-scroll';
                renderConstituencyTree(r.constituency_tree, scrollWrap);
                body.appendChild(scrollWrap);
            }

            card.appendChild(header);
            card.appendChild(body);
            container.appendChild(card);
        });
    } catch (e) {
        alert('Error: ' + e.message);
    } finally {
        btn.textContent = 'Parse';
        btn.disabled = false;
    }
});

// ==================== CONSTITUENCY TREE (CSS) ====================

function renderConstituencyTree(tree, container) {
    const ul = document.createElement('ul');
    ul.className = 'constituency-tree';
    ul.appendChild(createTreeNode(tree));
    container.appendChild(ul);
}

function createTreeNode(node) {
    if (!node) return document.createElement('span');

    const li = document.createElement('li');
    li.className = 'constituency-item';

    if (node.is_leaf) {
        li.innerHTML = `
            <div class="constituency-box constituency-leaf">
                <span class="constituency-leaf-tag">${escapeHtml(node.label)}</span>
                <span class="constituency-leaf-word">${escapeHtml(node.text)}</span>
            </div>`;
        return li;
    }

    const box = document.createElement('div');
    box.className = 'constituency-box constituency-node-box';
    box.textContent = node.label;
    li.appendChild(box);

    if (node.children && node.children.length) {
        const childUl = document.createElement('ul');
        childUl.className = 'constituency-children';
        node.children.forEach(child => {
            childUl.appendChild(createTreeNode(child));
        });
        li.appendChild(childUl);
    }

    return li;
}

// ==================== DICTIONARY TAB ====================

let dictOffset = 0;
const dictLimit = 20;

document.getElementById('dictSearchBtn').addEventListener('click', async () => {
    const q = document.getElementById('dictSearch').value.trim();
    if (!q) return;
    try {
        const res = await fetch(API + '/api/translate/dict/search?q=' + encodeURIComponent(q));
        const data = await res.json();
        document.getElementById('dictResults').style.display = '';
        document.getElementById('dictPag').style.display = 'none';
        renderDict(data.entries);
    } catch (e) { alert('Error: ' + e.message); }
});

document.getElementById('dictBootBtn').addEventListener('click', async () => {
    const btn = document.getElementById('dictBootBtn');
    btn.textContent = 'Loading...';
    btn.disabled = true;
    try {
        const res = await fetch(API + '/api/translate/dict/bootstrap', {method: 'POST'});
        const data = await res.json();
        alert(`Added ${data.added} common word pairs to dictionary`);
    } catch (e) { alert('Error: ' + e.message); }
    finally { btn.textContent = 'Bootstrap Common Words'; btn.disabled = false; }
});

document.getElementById('dictListBtn').addEventListener('click', async () => {
    dictOffset = 0;
    await loadDictPage();
});

document.getElementById('dictNext').addEventListener('click', async () => {
    dictOffset += dictLimit;
    await loadDictPage();
});

document.getElementById('dictPrev').addEventListener('click', async () => {
    dictOffset = Math.max(0, dictOffset - dictLimit);
    await loadDictPage();
});

async function loadDictPage() {
    try {
        const res = await fetch(API + `/api/translate/dict?limit=${dictLimit}&offset=${dictOffset}`);
        const data = await res.json();
        document.getElementById('dictResults').style.display = '';
        document.getElementById('dictPag').style.display = data.total > dictLimit ? '' : 'none';
        const page = Math.floor(dictOffset / dictLimit) + 1;
        const totalPages = Math.ceil(data.total / dictLimit);
        document.getElementById('dictPageInfo').textContent = `Page ${page} of ${totalPages} (${data.total} entries)`;
        renderDict(data.entries);
    } catch (e) { alert('Error: ' + e.message); }
}

function renderDict(entries) {
    const tbody = document.getElementById('dictBody');
    tbody.innerHTML = '';
    if (!entries || entries.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="padding:12px; text-align:center; color:var(--text-secondary);">No entries found.</td></tr>';
        return;
    }
    entries.forEach(e => {
        const tr = document.createElement('tr');
        tr.style.borderBottom = '1px solid var(--border)';
        tr.innerHTML = `
            <td style="padding:6px; font-weight:500;">${escapeHtml(e.source)}</td>
            <td style="padding:6px; color:var(--primary);">${escapeHtml(e.target)}</td>
            <td style="padding:6px; font-size:0.85rem;">${escapeHtml(e.source_pos)}</td>
            <td style="padding:6px; font-size:0.85rem;">${escapeHtml(e.target_pos)}</td>
            <td style="padding:6px;"><button class="btn btn-secondary" style="font-size:0.8rem; padding:2px 8px;" onclick="deleteDictEntry(${e.id})">Delete</button></td>
        `;
        tbody.appendChild(tr);
    });
}

async function deleteDictEntry(id) {
    if (!confirm('Delete this entry?')) return;
    try {
        await fetch(API + '/api/translate/dict/delete', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id})
        });
        await loadDictPage();
    } catch (e) { alert('Error: ' + e.message); }
}

function escapeHtml(text) {
    if (!text) return '';
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
               .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

// ==================== TXT EXPORT ====================

document.getElementById('tlExportBtn').addEventListener('click', async () => {
    const text = window._lastTlText;
    if (!text) return;

    const btn = document.getElementById('tlExportBtn');
    btn.textContent = 'Generating...';
    btn.disabled = true;

    try {
        const res = await fetch(API + '/api/translate/export', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text, filename: 'translation.txt'})
        });
        if (!res.ok) throw new Error('Export failed');

        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'translation.txt';
        a.click();
        URL.revokeObjectURL(url);
    } catch (e) {
        alert('Error: ' + e.message);
    } finally {
        btn.textContent = 'Download TXT';
        btn.disabled = false;
    }
});

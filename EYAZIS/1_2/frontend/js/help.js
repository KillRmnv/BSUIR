const API_BASE = '/api';

async function loadHelp() {
    try {
        const res = await fetch(`${API_BASE}/help`);
        const data = await res.json();
        renderTerms(data.theoretical_terms);
    } catch (err) {
        document.getElementById('termsContainer').innerHTML =
            `<div class="empty-state">Error loading help data: ${err.message}</div>`;
    }
}

function renderTerms(terms) {
    const container = document.getElementById('termsContainer');
    container.innerHTML = '';
    for (const [key, term] of Object.entries(terms)) {
        const card = document.createElement('div');
        card.className = 'term-card';
        let html = `
            <div class="term-name">${escapeHtml(term.term)}</div>
            <div class="term-definition">${escapeHtml(term.definition)}</div>
        `;
        if (term.formula) {
            html += `<div class="term-formula">${escapeHtml(term.formula)}</div>`;
        }
        card.innerHTML = html;
        container.appendChild(card);
    }
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

loadHelp();

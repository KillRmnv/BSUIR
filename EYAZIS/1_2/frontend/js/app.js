const API_BASE = '/api';

const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
const resultCount = document.getElementById('resultCount');
const keywords = document.getElementById('keywords');
const resultsList = document.getElementById('resultsList');
const modal = document.getElementById('helpModal');
const modalBody = document.getElementById('modalBody');
let lastQuery = '';

searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (!query) return;
    lastQuery = query;

    resultsList.innerHTML = '<div class="empty-state">Searching...</div>';
    searchResults.classList.remove('hidden');

    try {
        const res = await fetch(`${API_BASE}/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, top_k: 10 }),
        });
        const data = await res.json();

        if (data.error) {
            resultsList.innerHTML = `<div class="empty-state">${data.error}</div>`;
            return;
        }

        resultCount.textContent = `${data.total_found} result${data.total_found !== 1 ? 's' : ''}`;

        keywords.innerHTML = '';
        if (data.keywords && data.keywords.length > 0) {
            data.keywords.forEach(kw => {
                const tag = document.createElement('span');
                tag.className = 'keyword-tag';
                tag.textContent = kw;
                keywords.appendChild(tag);
            });
        }

        if (data.results.length === 0) {
            resultsList.innerHTML = '<div class="empty-state">No results found.</div>';
            return;
        }

        resultsList.innerHTML = '';
        data.results.forEach(doc => {
            const card = document.createElement('div');
            card.className = 'result-card';
            card.innerHTML = `
                <div class="result-card-header">
                    <span class="result-title">${escapeHtml(doc.title)}</span>
                    <span class="result-similarity">${(doc.similarity * 100).toFixed(1)}%</span>
                </div>
                <div class="result-snippet">${doc.highlighted_content || escapeHtml(doc.content)}</div>
                ${doc.matched_terms && doc.matched_terms.length ? `
                    <div class="result-matched">
                        <span class="matched-label">Matched:</span>
                        ${doc.matched_terms.map(t => `<span class="matched-tag">${escapeHtml(t)}</span>`).join('')}
                    </div>
                ` : ''}
            `;
            card.addEventListener('click', () => showDocPreview(doc.id));
            resultsList.appendChild(card);
        });
    } catch (err) {
        resultsList.innerHTML = `<div class="empty-state">Error: ${err.message}</div>`;
    }
});

async function showDocPreview(docId) {
    try {
        const url = lastQuery
            ? `${API_BASE}/documents/${docId}?query=${encodeURIComponent(lastQuery)}`
            : `${API_BASE}/documents/${docId}`;
        const res = await fetch(url);
        const doc = await res.json();
        document.getElementById('modalTitle') || null;
        modal.querySelector('h3').textContent = doc.title;
        modalBody.innerHTML = `<p>${doc.highlighted_content || escapeHtml(doc.content)}</p>`;
        modal.classList.remove('hidden');
    } catch (err) {
        alert('Failed to load document');
    }
}

function closeModal() {
    modal.classList.add('hidden');
}

modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
});

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

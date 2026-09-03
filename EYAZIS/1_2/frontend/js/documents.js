const API_BASE = '/api';

const documentsList = document.getElementById('documentsList');
const docCount = document.getElementById('docCount');
const modal = document.getElementById('helpModal');

async function loadDocuments() {
    try {
        const res = await fetch(`${API_BASE}/documents`);
        const data = await res.json();
        docCount.textContent = `${data.total} document${data.total !== 1 ? 's' : ''} in corpus`;

        if (data.documents.length === 0) {
            documentsList.innerHTML = '<div class="empty-state">No documents in the corpus. Upload some documents first.</div>';
            return;
        }

        documentsList.innerHTML = '';
        data.documents.forEach(doc => {
            const row = document.createElement('div');
            row.className = 'doc-row';
            row.innerHTML = `
                <div class="doc-info">
                    <div class="doc-title-line">
                        <span class="doc-id-badge">#${doc.id}</span>
                        <span class="doc-title">${escapeHtml(doc.title)}</span>
                    </div>
                    <div class="doc-date">${doc.date_added ? new Date(doc.date_added).toLocaleDateString() : 'Unknown date'}</div>
                </div>
                <div class="doc-actions">
                    <button class="btn btn-small btn-secondary" onclick="event.stopPropagation(); viewDocument(${doc.id})">View</button>
                    <button class="btn btn-small btn-danger" onclick="event.stopPropagation(); deleteDocument(${doc.id})">Delete</button>
                </div>
            `;
            row.addEventListener('click', () => viewDocument(doc.id));
            documentsList.appendChild(row);
        });
    } catch (err) {
        documentsList.innerHTML = `<div class="empty-state">Error loading documents: ${err.message}</div>`;
    }
}

async function viewDocument(docId) {
    try {
        const res = await fetch(`${API_BASE}/documents/${docId}`);
        const doc = await res.json();
        modal.querySelector('h3').textContent = doc.title;
        document.getElementById('modalBody').innerHTML = `<p>${escapeHtml(doc.content)}</p>`;
        modal.classList.remove('hidden');
    } catch (err) {
        alert('Failed to load document');
    }
}

async function deleteDocument(docId) {
    if (!confirm('Are you sure you want to delete this document?')) return;
    try {
        await fetch(`${API_BASE}/documents/${docId}`, { method: 'DELETE' });
        loadDocuments();
    } catch (err) {
        alert('Failed to delete document');
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

loadDocuments();

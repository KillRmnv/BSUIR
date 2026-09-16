const API_BASE = '/api';

const manualForm = document.getElementById('manualForm');
const fileForm = document.getElementById('fileForm');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const uploadStatus = document.getElementById('uploadStatus');

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        fileName.textContent = fileInput.files[0].name;
    } else {
        fileName.textContent = 'No file selected';
    }
});

manualForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('docTitle').value.trim();
    const content = document.getElementById('docContent').value.trim();

    if (!title || !content) {
        showStatus('Please fill in all fields.', 'error');
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, content }),
        });
        const data = await res.json();
        if (data.error) {
            showStatus(data.error, 'error');
        } else {
            showStatus('Document uploaded and indexed successfully.', 'success');
            manualForm.reset();
        }
    } catch (err) {
        showStatus('Error: ' + err.message, 'error');
    }
});

fileForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (fileInput.files.length === 0) {
        showStatus('Please select a file.', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const res = await fetch(`${API_BASE}/upload-file`, {
            method: 'POST',
            body: formData,
        });
        const data = await res.json();
        if (data.error) {
            showStatus(data.error, 'error');
        } else {
            showStatus('File uploaded and indexed successfully.', 'success');
            fileForm.reset();
            fileName.textContent = 'No file selected';
        }
    } catch (err) {
        showStatus('Error: ' + err.message, 'error');
    }
});

function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `upload-status ${type}`;
    uploadStatus.classList.remove('hidden');
    setTimeout(() => {
        uploadStatus.classList.add('hidden');
    }, 5000);
}

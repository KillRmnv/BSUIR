const API_BASE = '/api';

const evalForm = document.getElementById('evalForm');
const evalQueries = document.getElementById('evalQueries');
const addQueryBtn = document.getElementById('addQueryBtn');
const metricsResults = document.getElementById('metricsResults');

addQueryBtn.addEventListener('click', () => {
    const row = document.createElement('div');
    row.className = 'eval-query-row';
    row.innerHTML = `
        <input type="text" class="eval-query-input" placeholder="Search query...">
        <input type="text" class="eval-relevant-input" placeholder="Relevant doc IDs (comma-separated)">
    `;
    evalQueries.appendChild(row);
});

evalForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const queryRows = document.querySelectorAll('.eval-query-row');
    const queriesResults = [];

    for (const row of queryRows) {
        const query = row.querySelector('.eval-query-input').value.trim();
        const relevantStr = row.querySelector('.eval-relevant-input').value.trim();
        if (!query || !relevantStr) continue;

        const relevantIds = relevantStr.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n));

        // Run the actual search to know what the system retrieves
        let retrievedIds = [];
        try {
            const sres = await fetch(`${API_BASE}/search`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, top_k: 10 }),
            });
            const sdata = await sres.json();
            if (!sdata.error) {
                retrievedIds = (sdata.results || []).map(r => r.id);
            }
        } catch (err) {
            // ignore — retrieved stays empty, metrics will reflect it
        }

        queriesResults.push({ query, retrieved_ids: retrievedIds, relevant_ids: relevantIds });
    }

    if (queriesResults.length === 0) {
        alert('Please enter at least one query with relevant document IDs.');
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/metrics`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ queries_results: queriesResults }),
        });
        const data = await res.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        displayMetrics(data);
    } catch (err) {
        alert('Error: ' + err.message);
    }
});

function displayMetrics(data) {
    metricsResults.classList.remove('hidden');

    document.getElementById('avgPrecision').textContent = data.average_precision.toFixed(3);
    document.getElementById('avgRecall').textContent = data.average_recall.toFixed(3);
    document.getElementById('avgFscore').textContent = data.average_fscore.toFixed(3);

    if (data.chart) {
        document.getElementById('metricsChart').src = `data:image/png;base64,${data.chart}`;
        document.getElementById('chartContainer').classList.remove('hidden');
    }

    const tbody = document.getElementById('metricsTableBody');
    tbody.innerHTML = '';
    data.query_metrics.forEach(qm => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${escapeHtml(qm.query)}</td>
            <td>${qm.metrics.precision.toFixed(3)}</td>
            <td>${qm.metrics.recall.toFixed(3)}</td>
            <td>${qm.metrics.fscore.toFixed(3)}</td>
            <td>${qm.metrics.fscore_05.toFixed(3)}</td>
            <td>${qm.metrics.fscore_2.toFixed(3)}</td>
        `;
        tbody.appendChild(tr);
    });
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

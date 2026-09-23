(function () {
    var sourceEl = document.getElementById('source');
    var textInputEl = document.getElementById('textInput');
    var docInputEl = document.getElementById('docInput');
    var textEl = document.getElementById('text');
    var docSelectEl = document.getElementById('docSelect');
    var nSentencesEl = document.getElementById('nSentences');
    var nValEl = document.getElementById('nVal');
    var langEl = document.getElementById('lang');
    var btnEl = document.getElementById('summarizeBtn');
    var statusEl = document.getElementById('status');
    var statsEl = document.getElementById('summaryStats');
    var sentencesEl = document.getElementById('summarySentences');
    var keywordsEl = document.getElementById('keywords');
    var originalEl = document.getElementById('originalText');

    var documents = [];

    sourceEl.addEventListener('change', function () {
        if (sourceEl.value === 'text') {
            textInputEl.classList.remove('hidden');
            docInputEl.classList.add('hidden');
        } else {
            textInputEl.classList.add('hidden');
            docInputEl.classList.remove('hidden');
            loadDocuments();
        }
    });

    nSentencesEl.addEventListener('input', function () {
        nValEl.textContent = nSentencesEl.value;
    });

    btnEl.addEventListener('click', function () {
        var method = document.querySelector('input[name="method"]:checked').value;
        var n = parseInt(nSentencesEl.value, 10);
        var lang = langEl.value;

        if (sourceEl.value === 'text') {
            var text = textEl.value.trim();
            if (!text) { showStatus('Please enter some text.', true); return; }
            doSummarize({ text: text, method: method, n_sentences: n, lang: lang });
        } else {
            var docId = docSelectEl.value;
            if (!docId) { showStatus('Please select a document.', true); return; }
            doSummarizeDoc({ doc_id: parseInt(docId, 10), method: method, n_sentences: n });
        }
    });

    function loadDocuments() {
        fetch('/api/documents')
            .then(function (r) { return r.json(); })
            .then(function (data) {
                documents = data.documents || data;
                docSelectEl.innerHTML = '';
                if (!documents.length) {
                    docSelectEl.innerHTML = '<option value="">No documents found</option>';
                    return;
                }
                documents.forEach(function (doc) {
                    var opt = document.createElement('option');
                    opt.value = doc.id;
                    opt.textContent = '#' + doc.id + ' ' + doc.title + ' (' + (doc.lang || 'en') + ')';
                    docSelectEl.appendChild(opt);
                });
            })
            .catch(function () {
                docSelectEl.innerHTML = '<option value="">Error loading documents</option>';
            });
    }

    function doSummarize(payload) {
        showStatus('Summarizing...', false);
        btnEl.disabled = true;
        fetch('/api/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                btnEl.disabled = false;
                if (data.error) { showStatus(data.error, true); return; }
                showStatus('', false);
                renderResults(data, payload.text || '');
            })
            .catch(function (e) {
                btnEl.disabled = false;
                showStatus('Request failed: ' + e.message, true);
            });
    }

    function doSummarizeDoc(payload) {
        showStatus('Summarizing...', false);
        btnEl.disabled = true;
        fetch('/api/documents/' + payload.doc_id)
            .then(function (r) { return r.json(); })
            .then(function (doc) {
                var fullContent = doc.content || '';
                return fetch('/api/summarize-doc', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                }).then(function (r) { return r.json(); }).then(function (data) {
                    return { data: data, fullContent: fullContent };
                });
            })
            .then(function (result) {
                btnEl.disabled = false;
                var data = result.data;
                if (data.error) { showStatus(data.error, true); return; }
                showStatus('', false);
                renderResults(data, result.fullContent);
            })
            .catch(function (e) {
                btnEl.disabled = false;
                showStatus('Request failed: ' + e.message, true);
            });
    }

    function renderResults(data, originalText) {
        statsEl.innerHTML = '';
        statsEl.classList.remove('hidden');

        var methodLabel = data.method === 'textrank' ? 'TextRank' : 'Sentence Extraction';
        var statItems = [
            { label: 'Method', value: methodLabel },
            { label: 'Sentences', value: data.stats.selected + ' / ' + data.stats.total_sentences },
            { label: 'Time', value: data.stats.processing_time + 's' },
            { label: 'Compression', value: data.stats.compression_ratio + '%' }
        ];
        statItems.forEach(function (item) {
            var card = document.createElement('div');
            card.className = 'metric-card';
            card.innerHTML = '<div class="metric-value">' + escapeHtml(item.value) + '</div>' +
                '<div class="metric-label">' + escapeHtml(item.label) + '</div>';
            statsEl.appendChild(card);
        });

        sentencesEl.innerHTML = '';
        if (!data.sentences.length) {
            sentencesEl.innerHTML = '<p style="color:var(--text-light);">No sentences extracted.</p>';
        } else {
            data.sentences.forEach(function (s, idx) {
                var div = document.createElement('div');
                div.className = 'summary-sentence';
                div.innerHTML = '<span class="summary-rank">#' + (idx + 1) + '</span>' +
                    '<span class="summary-score">' + s.score.toFixed(4) + '</span>' +
                    '<span class="summary-text">' + escapeHtml(s.text) + '</span>';
                sentencesEl.appendChild(div);
            });
        }

        keywordsEl.innerHTML = '';
        if (data.keywords && data.keywords.length) {
            data.keywords.forEach(function (kw) {
                var tag = document.createElement('span');
                tag.className = 'keyword-tag';
                tag.textContent = kw;
                keywordsEl.appendChild(tag);
            });
        }

        if (originalText) {
            var sentences = data.sentences || [];
            var highlighted = originalText;
            sentences.forEach(function (s) {
                var escaped = s.text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                highlighted = highlighted.replace(
                    new RegExp(escaped, 'g'),
                    '<mark>' + escapeHtml(s.text) + '</mark>'
                );
            });
            originalEl.innerHTML = highlighted;
        }
    }

    function showStatus(msg, isError) {
        statusEl.textContent = msg;
        statusEl.className = 'upload-status' + (msg ? (isError ? ' error' : ' success') : '');
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function openDocFromQuery() {
        var docId = new URLSearchParams(location.search).get('doc');
        if (!docId) return;
        sourceEl.value = 'doc';
        if (docInputEl) docInputEl.classList.remove('hidden');
        if (textInputEl) textInputEl.classList.add('hidden');
        var tries = 0;
        var apply = function () {
            tries += 1;
            var found = false;
            for (var i = 0; i < docSelectEl.options.length; i++) {
                if (String(docSelectEl.options[i].value) === String(docId)) {
                    docSelectEl.value = String(docId);
                    found = true;
                    break;
                }
            }
            if (found) {
                btnEl.click();
            } else if (tries < 40) {
                setTimeout(apply, 150);
            } else {
                showStatus('Document #' + docId + ' not found.', true);
            }
        };
        setTimeout(apply, 250);
    }

    loadDocuments();
    openDocFromQuery();
})();

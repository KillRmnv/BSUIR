"""
Automatic document summarization engine.
Two extractive methods: TF-IDF Sentence Extraction and TextRank.
"""
import math
import re
import time
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

import numpy as np
from nltk.tokenize import sent_tokenize

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from search.document_processor import (
    clean_text, VOCAB, IDF, STEMMER,
    STOP_WORDS_EN, STOP_WORDS_FR, get_query_terms
)


def _split_sentences(text: str) -> List[str]:
    raw = sent_tokenize(text.strip())
    return [s.strip() for s in raw if s.strip()]


def _split_paragraphs(text: str) -> List[str]:
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def _sentence_paragraph_index(sent: str, paragraphs: List[str]) -> int:
    for i, p in enumerate(paragraphs):
        if sent in p:
            return i
    return 0


def _compute_tf(tokens: List[str]) -> Dict[str, float]:
    tf = Counter(tokens)
    total = len(tokens) if tokens else 1
    return {t: c / total for t, c in tf.items()}


# ─── Method A: TF-IDF Sentence Extraction ───────────────────────────

def sentence_extraction(text: str, n: int = 10, lang: str = 'en') -> Dict:
    t0 = time.time()

    sentences = _split_sentences(text)
    paragraphs = _split_paragraphs(text)
    if not sentences:
        return {'sentences': [], 'keywords': [], 'stats': {}}

    total_chars = len(text)

    all_tokens = clean_text(text, lang)
    doc_tf = _compute_tf(all_tokens)
    tf_max = max(doc_tf.values()) if doc_tf else 1.0

    para_char_offsets = []
    offset = 0
    for p in paragraphs:
        para_char_offsets.append(offset)
        offset += len(p) + 2

    scored = []
    for i, sent in enumerate(sentences):
        tokens = clean_text(sent, lang)
        if len(tokens) < 2:
            continue

        sent_tf = _compute_tf(tokens)

        score_tf = sum(
            sent_tf[t] * (0.5 + 0.5 * doc_tf.get(t, 0) / tf_max)
            for t in sent_tf
        )

        char_pos = text.find(sent)
        if char_pos < 0:
            char_pos = 0
        posd = 1.0 - (char_pos / total_chars) if total_chars > 0 else 1.0

        para_idx = _sentence_paragraph_index(sent, paragraphs)
        para_text = paragraphs[para_idx] if para_idx < len(paragraphs) else ''
        para_len = len(para_text) if para_text else 1
        chars_before_in_para = text.find(sent, para_char_offsets[para_idx]) - para_char_offsets[para_idx]
        if chars_before_in_para < 0:
            chars_before_in_para = 0
        posp = 1.0 - (chars_before_in_para / para_len) if para_len > 0 else 1.0

        final_score = score_tf * posd * posp

        scored.append({
            'id': i + 1,
            'text': sent,
            'score': round(final_score, 6),
            'position': i + 1
        })

    scored.sort(key=lambda x: x['score'], reverse=True)
    top = scored[:n]
    top.sort(key=lambda x: x['position'])

    keywords = _extract_keywords_from_text(text, lang=lang)

    elapsed = round(time.time() - t0, 4)
    compression = round(len(' '.join(s['text'] for s in top)) / len(text) * 100, 1) if text else 0

    return {
        'method': 'extraction',
        'sentences': top,
        'keywords': keywords,
        'stats': {
            'total_sentences': len(sentences),
            'selected': len(top),
            'processing_time': elapsed,
            'compression_ratio': compression
        }
    }


# ─── Method B: TextRank ────────────────────────────────────────────

def _build_similarity_matrix(sentences: List[str], lang: str) -> np.ndarray:
    n = len(sentences)
    if n <= 1:
        return np.zeros((1, 1))

    dim = min(len(VOCAB), 5000) if VOCAB else 5000

    vectors = []
    for sent in sentences:
        tokens = clean_text(sent, lang)
        vec = np.zeros(dim)
        tf = Counter(tokens)
        for token, count in tf.items():
            if token in VOCAB:
                idx = VOCAB[token]
                if idx < dim:
                    tf_val = 1 + math.log(count) if count > 0 else 0
                    idf_val = IDF.get(token, math.log(10) + 1)
                    vec[idx] = tf_val * idf_val
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        vectors.append(vec)

    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            cos_sim = float(np.dot(vectors[i], vectors[j]))
            if cos_sim > 0:
                matrix[i][j] = cos_sim
                matrix[j][i] = cos_sim

    return matrix


def _pagerank(matrix: np.ndarray, damping: float = 0.85,
              iterations: int = 50, tol: float = 1e-6) -> np.ndarray:
    n = matrix.shape[0]
    if n == 0:
        return np.array([])

    out_degree = matrix.sum(axis=1)
    adj = matrix.copy()

    for i in range(n):
        if out_degree[i] > 0:
            adj[i] = adj[i] / out_degree[i]

    pr = np.ones(n) / n

    for _ in range(iterations):
        new_pr = (1 - damping) / n + damping * adj.T @ pr
        if np.linalg.norm(new_pr - pr) < tol:
            break
        pr = new_pr

    return pr


def textrank(text: str, n: int = 10, lang: str = 'en') -> Dict:
    t0 = time.time()

    sentences = _split_sentences(text)
    if not sentences:
        return {'sentences': [], 'keywords': [], 'stats': {}}

    sim_matrix = _build_similarity_matrix(sentences, lang)
    pr_scores = _pagerank(sim_matrix)

    scored = []
    for i, sent in enumerate(sentences):
        scored.append({
            'id': i + 1,
            'text': sent,
            'score': round(float(pr_scores[i]), 6),
            'position': i + 1
        })

    scored.sort(key=lambda x: x['score'], reverse=True)
    top = scored[:n]
    top.sort(key=lambda x: x['position'])

    keywords = _extract_keywords_from_text(text, lang=lang)

    elapsed = round(time.time() - t0, 4)
    compression = round(len(' '.join(s['text'] for s in top)) / len(text) * 100, 1) if text else 0

    return {
        'method': 'textrank',
        'sentences': top,
        'keywords': keywords,
        'stats': {
            'total_sentences': len(sentences),
            'selected': len(top),
            'processing_time': elapsed,
            'compression_ratio': compression
        }
    }


# ─── Shared: keyword extraction ────────────────────────────────────

def _extract_keywords_from_text(text: str, top_k: int = 8, lang: str = 'en') -> List[str]:
    tokens = clean_text(text, lang)
    tf = Counter(tokens)
    scored = []
    for token, count in tf.items():
        tf_val = 1 + math.log(count) if count > 0 else 0
        idf_val = IDF.get(token, 1.0)
        scored.append((token, tf_val * idf_val))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [word for word, _ in scored[:top_k]]


# ─── Public API ────────────────────────────────────────────────────

def summarize(text: str, method: str = 'textrank', n_sentences: int = 10,
              lang: str = 'en') -> Dict:
    if method == 'extraction':
        return sentence_extraction(text, n_sentences, lang)
    elif method == 'textrank':
        return textrank(text, n_sentences, lang)
    else:
        raise ValueError(f"Unknown method: {method}. Use 'extraction' or 'textrank'.")

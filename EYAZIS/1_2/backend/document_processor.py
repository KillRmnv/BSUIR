import re
import math
import html as html_module
from collections import Counter
from typing import List, Dict, Tuple, Set
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

STEMMER = PorterStemmer()
STOP_WORDS = set(stopwords.words('english'))
VOCAB: Dict[str, int] = {}
IDF: Dict[str, float] = {}


def clean_text(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 1]
    tokens = [STEMMER.stem(t) for t in tokens]
    return tokens


def build_vocabulary(documents: List[str]) -> Dict[str, int]:
    global VOCAB
    doc_freq = Counter()
    for doc in documents:
        tokens = set(clean_text(doc))
        for token in tokens:
            doc_freq[token] += 1
    sorted_words = sorted(doc_freq.keys())
    VOCAB = {word: idx for idx, word in enumerate(sorted_words)}
    return VOCAB


def compute_idf(documents: List[str]) -> Dict[str, float]:
    global IDF
    n = len(documents)
    doc_freq = Counter()
    for doc in documents:
        tokens = set(clean_text(doc))
        for token in tokens:
            doc_freq[token] += 1
    IDF = {word: math.log(n / (freq + 1)) + 1 for word, freq in doc_freq.items()}
    return IDF


def vectorize_text(text: str) -> List[float]:
    tokens = clean_text(text)
    tf = Counter(tokens)
    dim = len(VOCAB)
    vector = [0.0] * dim
    for token, count in tf.items():
        if token in VOCAB:
            idx = VOCAB[token]
            tf_val = 1 + math.log(count) if count > 0 else 0
            idf_val = IDF.get(token, math.log(10) + 1)
            vector[idx] = tf_val * idf_val
    norm = math.sqrt(sum(v * v for v in vector))
    if norm > 0:
        vector = [v / norm for v in vector]
    return vector


def vectorize_text_with_dim(text: str, dim: int) -> List[float]:
    tokens = clean_text(text)
    tf = Counter(tokens)
    vector = [0.0] * dim
    for token, count in tf.items():
        if token in VOCAB:
            idx = VOCAB[token]
            if idx < dim:
                tf_val = 1 + math.log(count) if count > 0 else 0
                idf_val = IDF.get(token, math.log(10) + 1)
                vector[idx] = tf_val * idf_val
    norm = math.sqrt(sum(v * v for v in vector))
    if norm > 0:
        vector = [v / norm for v in vector]
    return vector


def get_vocab_size() -> int:
    return len(VOCAB)


def get_query_terms(query: str) -> List[str]:
    """Stemmed query tokens that actually contribute to the vector
    (present in VOCAB/IDF, i.e. not stop-words and not OOV)."""
    return [t for t in clean_text(query) if t in VOCAB or t in IDF]


def highlight_terms(text: str, terms: Set[str]) -> Tuple[str, List[str]]:
    """Escape text and wrap occurrences of `terms` (matched by stemmed form) in <mark>.
    Returns (html, matched_terms)."""
    escaped = html_module.escape(text)
    pattern = re.compile(r"[A-Za-z0-9']+")
    out = []
    last = 0
    matched = []
    seen = set()
    for m in pattern.finditer(escaped):
        word = m.group(0)
        stem = STEMMER.stem(word.lower().strip("'"))
        if stem in terms:
            if stem not in seen:
                seen.add(stem)
                matched.append(stem)
            out.append(escaped[last:m.start()])
            out.append(f"<mark>{word}</mark>")
        else:
            out.append(escaped[last:m.end()])
        last = m.end()
    out.append(escaped[last:])
    return "".join(out), matched


def highlight_snippet(
    content: str,
    terms: Set[str],
    max_len: int = 500,
    context: int = 160,
) -> Tuple[str, List[str]]:
    """Build a highlighted snippet of `content` around the first token that matches `terms`.
    If nothing matches, take the plain prefix. Returns (html, matched_terms)."""
    first_span = None
    for m in re.finditer(r"[A-Za-z0-9']+", content):
        stem = STEMMER.stem(m.group(0).lower().strip("'"))
        if stem in terms:
            first_span = m.span()
            break

    if first_span is None:
        snippet = content[:max_len]
    else:
        start, end = first_span
        s = max(0, start - context)
        e = min(len(content), end + context)
        snippet = ("…" if s > 0 else "") + content[s:e] + ("…" if e < len(content) else "")
        if len(snippet) > max_len:
            snippet = snippet[:max_len] + "…"

    return highlight_terms(snippet, terms)


def extract_keywords(text: str, top_k: int = 5) -> List[str]:
    tokens = clean_text(text)
    tf = Counter(tokens)
    scored = []
    for token, count in tf.items():
        tf_val = 1 + math.log(count) if count > 0 else 0
        idf_val = IDF.get(token, 1.0)
        scored.append((token, tf_val * idf_val))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [word for word, _ in scored[:top_k]]

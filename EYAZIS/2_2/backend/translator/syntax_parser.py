"""
Syntax parser for English and French using spaCy + NLTK RegexpParser.
Produces constituency trees in JSON format: {label, children, is_leaf, text}.
Ported from EYAZIS/4 SyntaxService.
"""
import logging
import spacy
from nltk import RegexpParser, Tree
from nltk.tokenize import sent_tokenize
from typing import List, Optional

logger = logging.getLogger(__name__)

# ── spaCy models (lazy load) ─────────────────────────────────────────
_NLP_EN = None
_NLP_FR = None


def _get_nlp(lang='en'):
    global _NLP_EN, _NLP_FR
    if lang == 'fr':
        if _NLP_FR is None:
            try:
                _NLP_FR = spacy.load("fr_core_news_sm")
            except OSError:
                logger.warning("spaCy model 'fr_core_news_sm' not installed.")
                _NLP_FR = False
        return _NLP_FR if _NLP_FR else None
    else:
        if _NLP_EN is None:
            try:
                _NLP_EN = spacy.load("en_core_web_sm")
            except OSError:
                logger.warning("spaCy model 'en_core_web_sm' not installed.")
                _NLP_EN = False
        return _NLP_EN if _NLP_EN else None


# ── Constituency grammars (universal POS tags, from EYAZIS/4) ────────
EN_GRAMMAR = r"""
    ADVP: {<ADV>+}
    ADJP: {<ADV>*<ADJ>+}
    NP: {<DET|NUM|ADJ>*<NOUN|PROPN>+}
        {<PRON>}
    PP: {<ADP><NP>}
    VP: {<AUX|VERB>+<PART>?<ADV>*<NP|PP|ADJP|ADVP>*}
    CLAUSE: {<NP><VP>}
"""

FR_GRAMMAR = r"""
    ADVP: {<ADV>+}
    ADJP: {<ADV>*<ADJ>+}
    NP: {<DET|NUM|ADJ>*<NOUN|PROPN>+}
        {<PRON>}
    PP: {<ADP><NP>}
    VP: {<AUX|VERB>+<PART>?<ADV>*<NP|PP|ADJP|ADVP>*}
    CLAUSE: {<NP><VP>}
"""

_EN_PARSER = RegexpParser(EN_GRAMMAR)
_FR_PARSER = RegexpParser(FR_GRAMMAR)


# ── Public API ───────────────────────────────────────────────────────

def parse_sentence(sentence: str, lang: str = 'en') -> Optional[Tree]:
    """Parse a single sentence into a constituency tree."""
    nlp = _get_nlp(lang)
    if nlp is None:
        return None

    doc = nlp(sentence)
    tagged = [(t.text, t.pos_) for t in doc if not t.is_space]
    if not tagged:
        return None

    parser = _FR_PARSER if lang == 'fr' else _EN_PARSER
    tree = parser.parse(tagged)
    if not isinstance(tree, Tree):
        tree = Tree("S", list(tree))
    return tree


def tree_to_constituency(tree) -> dict:
    """Convert an NLTK Tree to JSON constituency format.
    Format: {label, children, is_leaf, text} — matching EYAZIS/4."""
    if isinstance(tree, Tree):
        return {
            "label": tree.label(),
            "children": [tree_to_constituency(c) for c in tree],
        }
    # Leaf: (word, POS) tuple
    if isinstance(tree, tuple) and len(tree) == 2:
        word, tag = tree
        return {"label": tag, "text": word, "is_leaf": True}
    return {"label": str(tree), "text": str(tree), "is_leaf": True}


def tree_to_str(tree) -> str:
    """Pretty-print an NLTK Tree."""
    return str(tree)


def parse_text(text: str, lang: str = 'en') -> List[dict]:
    """Parse all sentences in text.
    Returns list of {sentence, constituency_tree, tree_str}.
    Supports 'en' (spaCy en_core_web_sm) and 'fr' (spaCy fr_core_news_sm)."""
    sentences = sent_tokenize(text.strip())
    results = []
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        tree = parse_sentence(sent, lang)
        if tree:
            results.append({
                "sentence": sent,
                "constituency_tree": tree_to_constituency(tree),
                "tree_str": tree_to_str(tree),
            })
    return results


def get_phrases(tree, phrase_label: str = "NP") -> List[str]:
    """Extract phrases of a given type from a parse tree."""
    phrases = []
    if isinstance(tree, Tree):
        if tree.label() == phrase_label:
            leaf_words = " ".join(leaf[0] if isinstance(leaf, tuple) else str(leaf)
                                  for leaf in tree.leaves())
            phrases.append(leaf_words)
        for child in tree:
            phrases.extend(get_phrases(child, phrase_label))
    return phrases

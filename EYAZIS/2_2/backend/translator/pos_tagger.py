"""
POS tagging for English and French using NLTK.
EN: averaged_perceptron_tagger
FR: rule-based fallback (NLTK's perceptron_tagger_fr may not be installed)
"""
import nltk
from typing import List, Tuple

try:
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except (LookupError, OSError):
    try:
        nltk.download('averaged_perceptron_tagger_eng', quiet=True)
    except Exception:
        pass

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except (LookupError, OSError):
    try:
        nltk.download('averaged_perceptron_tagger', quiet=True)
    except Exception:
        pass

try:
    nltk.data.find('tokenizers/punkt_tab')
except (LookupError, OSError):
    try:
        nltk.download('punkt_tab', quiet=True)
    except Exception:
        pass

try:
    nltk.data.find('tokenizers/punkt')
except (LookupError, OSError):
    try:
        nltk.download('punkt', quiet=True)
    except Exception:
        pass

try:
    nltk.data.find('taggers/perceptron_tagger_fr')
except (LookupError, OSError):
    try:
        nltk.download('perceptron_tagger_fr', quiet=True)
    except Exception:
        pass


# POS tag descriptions for display
POS_DESCRIPTIONS = {
    'CC': 'Coordinating conjunction',
    'CD': 'Cardinal number',
    'DT': 'Determiner',
    'EX': 'Existential there',
    'FW': 'Foreign word',
    'IN': 'Preposition or subordinating conjunction',
    'JJ': 'Adjective',
    'JJR': 'Adjective, comparative',
    'JJS': 'Adjective, superlative',
    'LS': 'List item marker',
    'MD': 'Modal',
    'NN': 'Noun, singular or mass',
    'NNS': 'Noun, plural',
    'NNP': 'Proper noun, singular',
    'NNPS': 'Proper noun, plural',
    'PDT': 'Predeterminer',
    'POS': 'Possessive ending',
    'PRP': 'Personal pronoun',
    'PRP$': 'Possessive pronoun',
    'RB': 'Adverb',
    'RBR': 'Adverb, comparative',
    'RBS': 'Adverb, superlative',
    'RP': 'Particle',
    'SYM': 'Symbol',
    'TO': 'to',
    'UH': 'Interjection',
    'VB': 'Verb, base form',
    'VBD': 'Verb, past tense',
    'VBG': 'Verb, gerund or present participle',
    'VBN': 'Verb, past participle',
    'VBP': 'Verb, non-3rd person singular present',
    'VBZ': 'Verb, 3rd person singular present',
    'WDT': 'Wh-determiner',
    'WP': 'Wh-pronoun',
    'WP$': 'Possessive wh-pronoun',
    'WRB': 'Wh-adverb',
    # French tags
    'NC': 'Common noun',
    'NPP': 'Proper noun',
    'V': 'Verb',
    'VINF': 'Verb, infinitive',
    'VPP': 'Verb, past participle',
    'VPR': 'Verb, present participle',
    'VMOD': 'Verb, modal',
    'ADJ': 'Adjective',
    'ADV': 'Adverb',
    'DET': 'Determiner',
    'PRE': 'Preposition',
    'CON': 'Conjunction',
    'PRO': 'Pronoun',
    'PONCT': 'Punctuation',
    'ABR': 'Abbreviation',
    'NUM': 'Number',
    'I': 'Interjection',
}


def pos_tag_en(text: str) -> List[Tuple[str, str]]:
    """POS tag English text. Returns list of (word, tag)."""
    tokens = nltk.word_tokenize(text)
    return nltk.pos_tag(tokens)


def pos_tag_fr(text: str) -> List[Tuple[str, str]]:
    """POS tag French text. Tries perceptron_tagger_fr, falls back to simple rules."""
    tokens = nltk.word_tokenize(text)
    try:
        return nltk.pos_tag(tokens, lang='fr')
    except Exception:
        return _pos_tag_fr_simple(tokens)


def _pos_tag_fr_simple(tokens: list) -> list:
    """Rule-based French POS tagging fallback."""
    determiners = {'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'au',
                   'aux', 'ce', 'cette', 'ces', 'mon', 'ma', 'mes', 'ton',
                   'ta', 'tes', 'son', 'sa', 'ses', 'notre', 'votre', 'leur'}
    prepositions = {'à', 'de', 'dans', 'sur', 'sous', 'avec', 'pour', 'par',
                    'en', 'sans', 'entre', 'chez', 'vers', 'depuis', 'pendant'}
    conjunctions = {'et', 'ou', 'mais', 'donc', 'car', 'ni', 'que', 'quand',
                    'comme', 'si', 'bien', 'quoique', 'bien que'}
    pronouns = {'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
                'me', 'te', 'se', 'lui', 'leur', 'y', 'en', 'qui', 'que',
                'quoi', 'dont', 'où'}
    articles = determiners

    result = []
    for token in tokens:
        lower = token.lower()
        if lower in articles:
            result.append((token, 'DET'))
        elif lower in prepositions:
            result.append((token, 'PRE'))
        elif lower in conjunctions:
            result.append((token, 'CON'))
        elif lower in pronouns:
            result.append((token, 'PRO'))
        elif token.endswith(('er', 'ir', 're', 'oir', 'eux')) and len(token) > 3:
            result.append((token, 'V'))
        elif token.endswith(('ment',)) and len(token) > 4:
            result.append((token, 'ADV'))
        elif token.endswith(('eux', 'if', 'ive', 'al', 'el', 'il', 'aire')):
            result.append((token, 'ADJ'))
        elif token[0].isupper() and len(token) > 1:
            result.append((token, 'NPP'))
        elif token.isdigit():
            result.append((token, 'NUM'))
        elif token in '.,;:!?()[]{}"\'-–—':
            result.append((token, 'PONCT'))
        else:
            result.append((token, 'NC'))
    return result


def tag_text(text: str, lang: str = 'en') -> List[Tuple[str, str]]:
    """Unified POS tagging interface."""
    if lang == 'fr':
        return pos_tag_fr(text)
    return pos_tag_en(text)


def get_pos_description(tag: str) -> str:
    """Get human-readable description of a POS tag."""
    return POS_DESCRIPTIONS.get(tag, f'Unknown ({tag})')

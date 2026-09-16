"""
Translation engine: word-by-word EN→FR translation using the dictionary.
Includes lemmatization, phrase matching, verb conjugation, and French grammar rules.
"""
import time
import re
from typing import Dict, List
from collections import Counter

from nltk.stem import WordNetLemmatizer
import nltk

from translator import dictionary
from translator.pos_tagger import tag_text, get_pos_description

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

lemmatizer = WordNetLemmatizer()

POS_MAP = {
    'VB': 'v', 'VBD': 'v', 'VBG': 'v', 'VBN': 'v', 'VBP': 'v', 'VBZ': 'v',
    'NN': 'n', 'NNS': 'n', 'NNP': 'n', 'NNPS': 'n',
    'JJ': 'a', 'JJR': 'a', 'JJS': 'a',
    'RB': 'r', 'RBR': 'r', 'RBS': 'r',
}

NEGATION_WORDS = {'not', "n't", 'never', 'no'}

FR_ARTICLES = {'un', 'une', 'le', 'la', 'les', 'du', 'de la', 'des', "l'", "l’"}

# Irregular verb conjugations: lemma -> {person: form}
# persons: 1sg, 2sg, 3sg, 1pl, 2pl, 3pl
IRREGULAR_VERBS = {
    'be': {
        'present': {'1sg': 'suis', '2sg': 'es', '3sg': 'est', '1pl': 'sommes', '2pl': 'êtes', '3pl': 'sont'},
        'imperfect': {'1sg': 'étais', '2sg': 'étais', '3sg': 'était', '1pl': 'étions', '2pl': 'étiez', '3pl': 'étaient'},
    },
    'have': {
        'present': {'1sg': 'ai', '2sg': 'as', '3sg': 'a', '1pl': 'avons', '2pl': 'avez', '3pl': 'ont'},
    },
    'do': {
        'present': {'1sg': 'fais', '2sg': 'fais', '3sg': 'fait', '1pl': 'faisons', '2pl': 'faites', '3pl': 'font'},
    },
    'go': {
        'present': {'1sg': 'vais', '2sg': 'vas', '3sg': 'va', '1pl': 'allons', '2pl': 'allez', '3pl': 'vont'},
    },
    'can': {
        'present': {'1sg': 'peux', '2sg': 'peux', '3sg': 'peut', '1pl': 'pouvons', '2pl': 'pouvez', '3pl': 'peuvent'},
    },
    'will': {
        'present': {'1sg': 'serai', '2sg': 'seras', '3sg': 'sera', '1pl': 'serons', '2pl': 'serez', '3pl': 'seront'},
    },
    'must': {
        'present': {'1sg': 'dois', '2sg': 'dois', '3sg': 'doit', '1pl': 'devons', '2pl': 'devez', '3pl': 'doivent'},
    },
    'shall': {
        'present': {'1sg': 'devrai', '2sg': 'devras', '3sg': 'devra', '1pl': 'devrons', '2pl': 'devrez', '3pl': 'devront'},
    },
    'should': {
        'present': {'1sg': 'devrais', '2sg': 'devrais', '3sg': 'devrait', '1pl': 'devrions', '2pl': 'devriez', '3pl': 'devraient'},
    },
    'would': {
        'present': {'1sg': 'voudrais', '2sg': 'voudrais', '3sg': 'voudrait', '1pl': 'voudrions', '2pl': 'voudriez', '3pl': 'voudraient'},
    },
    'could': {
        'present': {'1sg': 'pourrais', '2sg': 'pourrais', '3sg': 'pourrait', '1pl': 'pourrions', '2pl': 'pourriez', '3pl': 'pourraient'},
    },
    'may': {
        'present': {'1sg': 'peux', '2sg': 'peux', '3sg': 'peut', '1pl': 'pouvons', '2pl': 'pouvez', '3pl': 'peuvent'},
    },
    'might': {
        'present': {'1sg': 'pourrais', '2sg': 'pourrais', '3sg': 'pourrait', '1pl': 'pourrions', '2pl': 'pourriez', '3pl': 'pourraient'},
    },
}

# Irregular past participles
IRREGULAR_PAST_PARTICIPLES = {
    'be': 'été', 'have': 'eu', 'do': 'fait', 'go': 'été',
    'make': 'fait', 'take': 'pris', 'give': 'donné', 'come': 'venu',
    'see': 'vu', 'know': 'su', 'think': 'pensé', 'say': 'dit',
    'get': 'obtenu', 'put': 'mis', 'find': 'trouvé', 'tell': 'dit',
    'ask': 'demandé', 'work': 'travaillé', 'seem': 'semblé', 'feel': 'senti',
    'try': 'essayé', 'leave': 'quitté', 'call': 'appelé', 'need': 'eu besoin',
    'become': 'devenu', 'keep': 'gardé', 'let': 'laissé', 'begin': 'commencé',
    'show': 'montré', 'hear': 'entendu', 'play': 'joué', 'run': 'couru',
    'move': 'bougé', 'live': 'vécu', 'believe': 'cru', 'bring': 'apporté',
    'happen': 'arrivé', 'write': 'écrit', 'provide': 'fourni', 'sit': 'assis',
    'stand': 'tenu', 'lose': 'perdu', 'pay': 'payé', 'meet': 'rencontré',
    'include': 'inclus', 'continue': 'continué', 'set': 'défini', 'learn': 'appris',
    'change': 'changé', 'lead': 'mené', 'understand': 'compris', 'watch': 'regardé',
    'follow': 'suivi', 'stop': 'arrêté', 'create': 'créé', 'speak': 'parlé',
    'read': 'lu', 'spend': 'dépensé', 'grow': 'grandi', 'open': 'ouvert',
    'walk': 'marché', 'win': 'gagné', 'offer': 'offert', 'remember': 'souvenu',
    'love': 'aimé', 'consider': 'considéré', 'appear': 'apparu', 'buy': 'acheté',
    'wait': 'attendu', 'serve': 'servi', 'die': 'mort', 'send': 'envoyé',
    'expect': 'attendu', 'build': 'construit', 'stay': 'resté', 'fall': 'tombé',
    'cut': 'coupé', 'reach': 'atteint', 'remain': 'resté', 'suggest': 'suggéré',
    'raise': 'élevé', 'pass': 'passé', 'sell': 'vendu', 'require': 'nécessité',
    'report': 'rapporté', 'decide': 'décidé', 'develop': 'développé', 'eat': 'mangé',
    'translate': 'traduit', 'implement': 'implémenté', 'analyze': 'analysé',
    'compare': 'comparé', 'observe': 'observé', 'measure': 'mesuré',
    'calculate': 'calculé', 'design': 'conçu', 'evaluate': 'évalué',
    'describe': 'décrit', 'explain': 'expliqué', 'discuss': 'discuté',
    'present': 'présenté', 'propose': 'proposé', 'conclude': 'conclu',
    'determine': 'déterminé', 'establish': 'établi', 'identify': 'identifié',
    'examine': 'examiné', 'investigate': 'enquêté', 'demonstrate': 'démontré',
    'illustrate': 'illustré', 'reveal': 'révélé', 'indicate': 'indiqué',
    'represent': 'représenté', 'contain': 'contenu', 'consist': 'consisté',
    'depend': 'dépendu', 'affect': 'affecté', 'influence': 'influencé',
    'cause': 'causé', 'produce': 'produit', 'receive': 'reçu', 'obtain': 'obtenu',
    'generate': 'généré', 'compute': 'calculé', 'process': 'traité',
    'store': 'stocké', 'transmit': 'transmis', 'convert': 'converti',
    'transform': 'transformé', 'apply': 'appliqué', 'combine': 'combiné',
    'separate': 'séparé', 'select': 'sélectionné', 'extract': 'extrait',
    'filter': 'filtré', 'sort': 'trié', 'merge': 'fusionné', 'classify': 'classé',
    'group': 'groupé', 'organize': 'organisé', 'manage': 'géré', 'control': 'contrôlé',
    'monitor': 'surveillé', 'optimize': 'optimisé', 'improve': 'amélioré',
    'enhance': 'amélioré', 'modify': 'modifié', 'update': 'mis à jour',
    'configure': 'configuré', 'initialize': 'initialisé', 'execute': 'exécuté',
    'perform': 'effectué', 'operate': 'opéré', 'connect': 'connecté',
    'disconnect': 'déconnecté', 'copy': 'copié', 'delete': 'supprimé',
    'save': 'sauvegardé', 'load': 'chargé', 'download': 'téléchargé',
    'upload': 'téléversé', 'search': 'recherché', 'browse': 'parcouru',
    'navigate': 'navigué', 'display': 'affiché', 'print': 'imprimé',
    'record': 'enregistré', 'start': 'démarré', 'restart': 'redémarré',
    'reset': 'réinitialisé', 'cancel': 'annulé', 'confirm': 'confirmé',
    'validate': 'validé', 'verify': 'vérifié', 'check': 'vérifié',
    'debug': 'débogué', 'trace': 'tracé', 'log': 'journalisé',
    'notify': 'notifié', 'alert': 'alerté', 'warn': 'averti',
    'request': 'demandé', 'respond': 'répondu', 'accept': 'accepté',
    'reject': 'rejeté', 'approve': 'approuvé', 'allow': 'permis',
    'restrict': 'restreint', 'lock': 'verrouillé', 'unlock': 'déverrouillé',
    'encrypt': 'chiffré', 'decrypt': 'déchiffré', 'authenticate': 'authentifié',
    'authorize': 'autorisé',
}

# -er verb conjugation (regular)
def _conjugate_er(infinitive: str, person: str) -> str:
    stem = infinitive[:-2]  # remove -er
    table = {
        '1sg': stem + 'e', '2sg': stem + 'es', '3sg': stem + 'e',
        '1pl': stem + 'ons', '2pl': stem + 'ez', '3pl': stem + 'ent',
    }
    return table.get(person, infinitive)

# -ir verb conjugation (regular)
def _conjugate_ir(infinitive: str, person: str) -> str:
    stem = infinitive[:-2]  # remove -ir
    table = {
        '1sg': stem + 'is', '2sg': stem + 'is', '3sg': stem + 'it',
        '1pl': stem + 'issons', '2pl': stem + 'issez', '3pl': stem + 'issent',
    }
    return table.get(person, infinitive)

# -re verb conjugation (regular)
def _conjugate_re(infinitive: str, person: str) -> str:
    stem = infinitive[:-2]  # remove -re
    table = {
        '1sg': stem + 's', '2sg': stem + 's', '3sg': stem,
        '1pl': stem + 'ons', '2pl': stem + 'ez', '3pl': stem + 'ent',
    }
    return table.get(person, infinitive)


def _get_person_from_subject(prev_words: list) -> str:
    """Determine grammatical person from the subject word preceding the verb."""
    if not prev_words:
        return '3sg'
    subject = prev_words[-1].lower()
    subject_map = {
        'i': '1sg', 'you': '2sg', 'he': '3sg', 'she': '3sg', 'it': '3sg',
        'we': '1pl', 'they': '3pl',
    }
    return subject_map.get(subject, '3sg')


def _conjugate_verb(infinitive: str, person: str, tense: str = 'present') -> str:
    """Conjugate a French verb for the given person and tense."""
    lower = infinitive.lower()
    # Check irregular verbs first
    if lower in IRREGULAR_VERBS:
        tenses = IRREGULAR_VERBS[lower]
        if tense in tenses:
            return tenses[tense].get(person, infinitive)
        # fallback to present
        return tenses.get('present', {}).get(person, infinitive)
    # Regular conjugation
    if lower.endswith('er'):
        return _conjugate_er(lower, person)
    if lower.endswith('ir'):
        return _conjugate_ir(lower, person)
    if lower.endswith('re'):
        return _conjugate_re(lower, person)
    return infinitive


def _get_past_participle(lemma: str) -> str:
    """Get the past participle of a French verb."""
    if lemma in IRREGULAR_PAST_PARTICIPLES:
        return IRREGULAR_PAST_PARTICIPLES[lemma]
    if lemma.endswith('er'):
        return lemma[:-2] + 'é'
    if lemma.endswith('ir'):
        return lemma[:-2] + 'i'
    if lemma.endswith('re'):
        return lemma[:-2] + 'u'
    return lemma


def _is_article_or_pronoun(fr_word: str) -> bool:
    """Check if a French word is already an article, pronoun, or determiner."""
    w = fr_word.lower().strip()
    return w in FR_ARTICLES or w in {
        'je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles',
        'me', 'te', 'se', 'lui', 'leur', 'y', 'en',
        'mon', 'ma', 'mes', 'ton', 'ta', 'tes', 'son', 'sa', 'ses',
        'notre', 'nos', 'votre', 'vos', 'leur', 'leurs',
        'ce', 'cette', 'ces', 'cet',
        'quel', 'quelle', 'quels', 'quelles',
        'qui', 'que', 'quoi', 'où', 'dont', 'lequel', 'laquelle',
    }


def _lemmatize(word: str, pos_tag: str = '') -> str:
    wn_pos = POS_MAP.get(pos_tag, 'n')
    return lemmatizer.lemmatize(word.lower(), pos=wn_pos)


def _lookup_with_lemma(word: str, pos: str = '') -> list:
    lower = word.lower()
    entries = dictionary.lookup(lower, pos)
    if entries:
        return entries
    lemma = _lemmatize(lower, pos)
    if lemma != lower:
        entries = dictionary.lookup(lemma, pos)
        if entries:
            return entries
    entries = dictionary.lookup(lower)
    if entries:
        return entries
    if lemma != lower:
        entries = dictionary.lookup(lemma)
        if entries:
            return entries
    return []


def translate_text(text: str) -> Dict:
    t0 = time.time()
    tagged = tag_text(text, lang='en')
    words = []
    translated_tokens = []
    translated_count = 0
    i = 0

    while i < len(tagged):
        word, pos = tagged[i]

        # Phrase matching (3-word, then 2-word)
        phrase_match = None
        for length in (3, 2):
            if i + length <= len(tagged):
                candidate = tuple(t[0].lower() for t in tagged[i:i+length])
                phrase_match = dictionary.lookup_phrase(candidate)
                if phrase_match:
                    break
        if phrase_match:
            fr_phrase = phrase_match["target"]
            translated_tokens.append(fr_phrase)
            translated_count += 1
            words.append({
                "en": " ".join(t[0] for t in tagged[i:i+phrase_match["length"]]),
                "fr": fr_phrase,
                "pos_en": "PHRASE",
                "pos_en_desc": "Multi-word expression",
                "translated": True,
            })
            i += phrase_match["length"]
            continue

        # Skip punctuation
        if len(word) <= 1 and not word.isalpha():
            translated_tokens.append(word)
            words.append({
                "en": word, "fr": word,
                "pos_en": pos, "pos_en_desc": get_pos_description(pos),
                "translated": False,
            })
            i += 1
            continue

        # Look up translation
        entries = _lookup_with_lemma(word, pos)
        if entries:
            best = entries[0]
            fr_word = best["target"]

            # Apply grammar rules — always apply for articles (need gender context)
            if word.lower() not in ('a', 'an', 'the', 'this', 'that', 'these', 'those'):
                if not _is_article_or_pronoun(fr_word):
                    fr_word = _apply_fr_rules(word, pos, fr_word, tagged, i, entries)
            else:
                fr_word = _apply_fr_rules(word, pos, fr_word, tagged, i, entries)

            translated_tokens.append(fr_word)
            translated_count += 1
            words.append({
                "en": word, "fr": fr_word,
                "pos_en": pos, "pos_en_desc": get_pos_description(pos),
                "translated": True,
            })
        else:
            translated_tokens.append(word)
            words.append({
                "en": word, "fr": word,
                "pos_en": pos, "pos_en_desc": get_pos_description(pos),
                "translated": False,
            })
        i += 1

    translated_tokens = _apply_negation(translated_tokens)
    translated_text = _rebuild_text(translated_tokens)
    word_count = len([w for w in tagged if w[0].isalpha()])
    elapsed = round(time.time() - t0, 4)

    return {
        "translated_text": translated_text,
        "word_count": word_count,
        "translated_count": translated_count,
        "words": words,
        "stats": {
            "total_words": word_count,
            "translated": translated_count,
            "coverage": round(translated_count / word_count * 100, 1) if word_count else 0,
            "processing_time": elapsed,
        }
    }


def _apply_fr_rules(en_word: str, pos: str, fr_word: str,
                     tagged: list, idx: int, entries: list) -> str:
    lower = en_word.lower()

    # Verb conjugation (not modals — they're already in dictionary as single forms)
    if pos.startswith('VB') and pos != 'VBG' and lower not in {
        'can', 'will', 'must', 'shall', 'may', 'should', 'would', 'could', 'might'
    }:
        person = _get_person_from_subject(
            [t[0] for t in tagged[max(0, idx-3):idx]]
        )
        fr_word = _conjugate_verb(fr_word, person, tense='present')
        return fr_word

    # Past tense: VBD -> past participle with avoir/être
    if pos == 'VBD':
        person = _get_person_from_subject(
            [t[0] for t in tagged[max(0, idx-3):idx]]
        )
        lemma = _lemmatize(lower, pos)
        # Find FR lemma from dictionary
        fr_lemma = fr_word
        pp = _get_past_participle(fr_lemma)
        # Simple past: subject + avoir + past participle
        avoir_forms = {'1sg': 'ai', '2sg': 'as', '3sg': 'a', '1pl': 'avons', '2pl': 'avez', '3pl': 'ont'}
        avoir = avoir_forms.get(person, 'a')
        return f"{avoir} {pp}"

    # a/an -> un/une (only if next FR word is a noun, guessed by gender)
    if lower in ('a', 'an', 'one'):
        if idx + 1 < len(tagged):
            next_fr = _lookup_with_lemma(tagged[idx+1][0], tagged[idx+1][1])
            if next_fr:
                gender = _guess_fr_gender(next_fr[0]["target"])
                return 'une' if gender == 'f' else 'un'
        return 'un'

    # the -> le/la/les
    if lower == 'the':
        if idx + 1 < len(tagged):
            next_fr = _lookup_with_lemma(tagged[idx+1][0], tagged[idx+1][1])
            if next_fr:
                next_target = next_fr[0]["target"]
                if next_target.endswith(('s', 'x')) or next_target in ('-s', '-x'):
                    return 'les'
                gender = _guess_fr_gender(next_target)
                return 'la' if gender == 'f' else 'le'
        return 'le'

    # this/that -> ce/cette (gender of next FR word)
    if lower in ('this', 'that'):
        if idx + 1 < len(tagged):
            next_fr = _lookup_with_lemma(tagged[idx+1][0], tagged[idx+1][1])
            if next_fr:
                gender = _guess_fr_gender(next_fr[0]["target"])
                return 'cette' if gender == 'f' else 'ce'
        return 'ce'

    # these/those -> ces
    if lower in ('these', 'those'):
        return 'ces'

    # is/are/was/were -> already conjugated by irregular verb lookup
    # (they come from dictionary, not conjugation rules)

    return fr_word


def _guess_fr_gender(fr_word: str) -> str:
    """Guess French gender from the FRENCH word ending."""
    word = fr_word.lower().strip()
    # Remove trailing consonants that aren't part of the ending pattern
    if word.endswith(('s', 'x', 'z')):
        word = word[:-1]
    # Masculine endings
    if word.endswith(('age', 'ment', 'eur', 'eau', 'ien', 'isme', 'oir', 'é', 'in', 'on', 'an')):
        return 'm'
    # Feminine endings
    if word.endswith(('tion', 'sion', 'ure', 'ence', 'ance', 'ette', 'ie', 'ée',
                       'ière', 'ique', 'ale', 'ole', 'ure', 'oi', 'ée',
                       'té', 'ure', 'ence', 'ance', 'ance')):
        return 'f'
    # Words ending in -e are often feminine
    if word.endswith('e') and not word.endswith(('ème', 'isme')):
        return 'f'
    return 'm'


def _apply_negation(tokens: list) -> list:
    result = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.lower() in NEGATION_WORDS or (token.endswith("n't") and len(token) > 3):
            if i + 1 < len(tokens):
                result.append('ne')
                result.append(tokens[i + 1])
                result.append('pas')
                i += 2
                continue
        result.append(token)
        i += 1
    return result


def _rebuild_text(tokens: list) -> str:
    if not tokens:
        return ""
    FR_PUNCT_BEFORE = {':', ';', '!', '?'}
    result = tokens[0]
    for i in range(1, len(tokens)):
        tok = tokens[i]
        prev = tokens[i - 1]
        # French spacing: space before : ; ! ?
        if tok in FR_PUNCT_BEFORE:
            result += " " + tok
        # No space before . , ) ; ! ?
        elif tok in {'.', ',', ')', ']', '}', ';', '!', '?'} or tok.startswith("'"):
            result += tok
        # No space after ( [ { " ' at the end of previous token
        elif prev in {'(', '[', '{', '"', "'"}:
            result += tok
        else:
            result += " " + tok
    return result


def get_frequency_list(text: str) -> List[dict]:
    tagged = tag_text(text, lang='en')
    freq = Counter()
    pos_map = {}
    for word, pos in tagged:
        if not word.isalpha():
            continue
        lower = word.lower()
        freq[lower] += 1
        if lower not in pos_map:
            pos_map[lower] = pos

    result = []
    for word, count in freq.most_common():
        pos = pos_map.get(word, "")
        entries = _lookup_with_lemma(word, pos)
        fr_translations = [e["target"] for e in entries[:3]]
        lemma = _lemmatize(word, pos)
        result.append({
            "en": word,
            "fr": ", ".join(fr_translations) if fr_translations else "—",
            "pos": pos,
            "pos_desc": get_pos_description(pos),
            "freq": count,
            "lemma": lemma if lemma != word else "",
        })
    return result


def add_to_dictionary(source: str, target: str, source_pos: str = "",
                      target_pos: str = "") -> bool:
    return dictionary.add_entry(source, target, source_pos, target_pos)

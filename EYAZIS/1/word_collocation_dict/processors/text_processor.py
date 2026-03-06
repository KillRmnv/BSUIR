"""Модуль для обработки текста и извлечения словосочетаний."""
import spacy
from typing import List, Tuple, Set
from collections import Counter


try:
    nlp = spacy.load("en_core_web_sm")
except (OSError, IOError):
    nlp = None


class TextProcessor:
    """Класс для обработки текста и извлечения словосочетаний."""
    
    def __init__(self, language: str = 'en'):
        self.language = language
        self.nlp = nlp
        if not self.nlp:
            raise RuntimeError("Модель spaCy не загружена")
    
    def extract_words(self, text: str) -> List[Tuple[str, str]]:
        doc = self.nlp(text)
        words = []
        for token in doc:
            if not token.is_stop and not token.is_punct and not token.is_space:
                lemma = token.lemma_.lower()
                pos = token.pos_
                words.append((lemma, pos))
        return words
        
    def extract_collocations(self, text: str) -> List[Tuple[str, int]]:
            """
            Извлекает словосочетания в виде естественных строк ("write code", "hard work").
            Использует позицию слов в предложении для правильного склеивания.
            """
            doc = self.nlp(text)
            phrases = []

            # amod:     adj + noun      (red car)
            # compound: noun + noun     (data science)
            # dobj:     verb + noun     (write code)
            # nsubj:    noun + verb     (error occurred)
            # advmod:   verb + adv      (run fast)
            # acomp:    verb + adj      (feels good)
            # prep:     verb + prep     (depend on) 
            # prt:      verb + particle (shut down)
            target_deps = {"amod", "compound", "dobj", "nsubj", "advmod", "acomp", "prep", "prt"}

            for token in doc:
                if token.is_punct or token.is_space:
                    continue

                for child in token.children:
                    if child.dep_ not in target_deps:
                        continue

                    if child.dep_ not in ['prep', 'prt'] and (child.is_stop or child.is_punct):
                        continue

                   
                    w1, w2 = sorted([token, child], key=lambda t: t.i)
                    
                    phrase = f"{w1.lemma_.lower()} {w2.lemma_.lower()}"
                    phrases.append(phrase)

            counts = Counter(phrases)
            return [(phrase, count) for phrase, count in counts.items()]


    

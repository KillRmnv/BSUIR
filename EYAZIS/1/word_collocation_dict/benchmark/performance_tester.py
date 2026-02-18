"""Модуль для тестирования производительности."""

import time
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class PerformanceTester:
    """Класс для тестирования производительности операций."""

    def __init__(self):
        self.results = []

    def test_text_processing(self, processor, texts_dict: Dict[str, str]) -> str:
        """Тест производительности обработки текста."""
        results = ["=== Тест обработки текста ===\n"]

        try:
            for name, text in texts_dict.items():
                start_time = time.perf_counter()
                words = processor.extract_words(text)
                words_time = time.perf_counter() - start_time

                start_time = time.perf_counter()
                collocations = processor.extract_collocations(text)
                colloc_time = time.perf_counter() - start_time

                results.append(f"{name}:")
                results.append(
                    f"  Извлечение слов: {words_time:.3f} сек ({len(words)} слов)"
                )
                results.append(
                    f"  Извлечение словосочетаний: {colloc_time:.3f} сек ({len(collocations)} сочетаний)"
                )
                results.append(f"  Общее время: {words_time + colloc_time:.3f} сек\n")

        except Exception as e:
            results.append(f"Ошибка: {e}")
            logger.exception("Ошибка при тестировании обработки текста")

        return "\n".join(results)

    def test_search_performance(self, db, words: List[Any], queries: List[str]) -> str:
        """Тест производительности поиска."""
        results = ["=== Тест поиска в словаре ===\n"]

        if not words:
            results.append(
                "Словарь пуст. Загрузите и обработайте текст для тестирования."
            )
            return "\n".join(results)

        results.append(f"Всего слов в словаре: {len(words)}\n")

        for query in queries:
            start_time = time.perf_counter()
            found = db.search_words(query)
            search_time = time.perf_counter() - start_time
            results.append(
                f"Поиск '{query}': {search_time:.4f} сек, найдено: {len(found)}"
            )

        results.append("\n")

        if words:
            test_lemmas = [words[i].lemma for i in range(min(5, len(words)))]
            results.append("Получение словосочетаний:")
            for lemma in test_lemmas:
                start_time = time.perf_counter()
                collocs = db.get_word_collocations(lemma)
                colloc_time = time.perf_counter() - start_time
                results.append(
                    f"  '{lemma}': {colloc_time:.4f} сек ({len(collocs)} сочетаний)"
                )

        return "\n".join(results)

    def test_filter_performance(
        self,
        words: List[Any],
        pos_list: List[str],
        text_prefixes: List[str],
    ) -> str:
        """Тест производительности фильтрации."""
        results = ["=== Тест фильтрации словаря ===\n"]

        if not words:
            results.append(
                "Словарь пуст. Загрузите и обработайте текст для тестирования."
            )
            return "\n".join(results)

        results.append(f"Всего слов в словаре: {len(words)}\n")

        results.append("Фильтрация по части речи:")
        for pos in pos_list:
            start_time = time.perf_counter()
            filtered = [w for w in words if w.pos == pos]
            filter_time = time.perf_counter() - start_time
            results.append(f"  {pos}: {filter_time:.4f} сек ({len(filtered)} слов)")

        results.append("\nТекстовая фильтрация (startswith):")
        for prefix in text_prefixes:
            start_time = time.perf_counter()
            filtered = [w for w in words if w.lemma.lower().startswith(prefix.lower())]
            filter_time = time.perf_counter() - start_time
            results.append(
                f"  '{prefix}*': {filter_time:.4f} сек ({len(filtered)} слов)"
            )

        return "\n".join(results)

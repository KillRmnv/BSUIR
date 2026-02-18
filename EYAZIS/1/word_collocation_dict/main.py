"""Главный файл для запуска приложения."""
import logging
import sys

from PyQt6.QtWidgets import QApplication

from word_collocation_dict.ui.main_window import MainWindow


def setup_logging():
    """Настройка вывода логов в консоль для отладки."""
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    if not root.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        root.addHandler(handler)


def main():
    """Точка входа в приложение."""
    setup_logging()
    log = logging.getLogger(__name__)
    log.debug("Запуск приложения: инициализация QApplication")
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    log.debug("Создание и отображение главного окна")
    window = MainWindow()
    window.show()
    log.debug("Приложение готово, запуск цикла событий")
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

import logging
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session, joinedload
from typing import Optional

logger = logging.getLogger(__name__)
Base = declarative_base()

word_collocation_association = Table(
    "word_collocation",
    Base.metadata,
    Column("word_id", Integer, ForeignKey("words.id"), primary_key=True),
    Column("collocation_id", Integer, ForeignKey("collocations.id"), primary_key=True),
)


class Word(Base):
    """Модель слова в словаре."""

    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lemma = Column(String(255), nullable=False, unique=True, index=True)  # Лемма слова
    pos = Column(String(50))  # Часть речи (Part of Speech)

    collocations = relationship(
        "Collocation", secondary=word_collocation_association, back_populates="words"
    )

    def __repr__(self):
        return f"<Word(lemma='{self.lemma}', pos='{self.pos}')>"


class Collocation(Base):
    """Модель словосочетания."""

    __tablename__ = "collocations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phrase = Column(String(500), nullable=False, unique=True, index=True)
    frequency = Column(Integer, default=0)
    source_text = Column(Text)

    words = relationship(
        "Word", secondary=word_collocation_association, back_populates="collocations"
    )

    def __repr__(self):
        return f"<Collocation(phrase='{self.phrase}', frequency={self.frequency})>"


class DictionaryDB:
    def __init__(self, db_path: str = "collocation_dict.db"):
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        """Создает новую сессию базы данных."""
        return self.SessionLocal()

    def add_word(self, lemma: str, pos: Optional[str] = None) -> Word:
        session = self.get_session()
        try:
            word = session.query(Word).filter_by(lemma=lemma).first()
            if not word:
                word = Word(lemma=lemma, pos=pos)
                session.add(word)
                session.commit()
                session.refresh(word)
            return word
        finally:
            session.close()

    def add_collocation(
        self,
        phrase: str,
        word_lemmas: list[str],
        frequency: int = 1,
        source_text: Optional[str] = None,
    ) -> Optional[Collocation]:
        session = self.get_session()
        try:
            collocation = session.query(Collocation).filter_by(phrase=phrase).first()

            if not collocation:
                collocation = Collocation(
                    phrase=phrase, frequency=frequency, source_text=source_text
                )
                session.add(collocation)
            else:
                collocation.frequency += frequency

            for lemma in word_lemmas:
                word = session.query(Word).filter_by(lemma=lemma).first()
                if word:
                    if word not in collocation.words:
                        collocation.words.append(word)

            session.commit()
            session.refresh(collocation)
            return collocation
        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка при добавлении словосочетания '{phrase}': {e}")
            return None
        finally:
            session.close()

    def get_word_collocations(self, lemma: str) -> list[Collocation]:
        session = self.get_session()
        try:
            word = session.query(Word).filter_by(lemma=lemma).first()
            if word:
                filtered_collocations = []
                for colloc in word.collocations:
                    phrase_words = colloc.phrase.lower().split()
                    if lemma.lower() in phrase_words:
                        filtered_collocations.append(colloc)
                return filtered_collocations
            return []
        finally:
            session.close()

    def search_words(self, query: str) -> list[Word]:

        session = self.get_session()
        try:
            return (
                session.query(Word)
                .options(joinedload(Word.collocations))
                .filter(Word.lemma.like(f"%{query}%"))
                .all()
            )
        finally:
            session.close()

    def get_all_words(self, order_by: str = "lemma") -> list[Word]:
        session = self.get_session()
        try:
            q = session.query(Word).options(joinedload(Word.collocations))
            if order_by == "pos":
                return q.order_by(Word.pos, Word.lemma).all()
            return q.order_by(Word.lemma).all()
        finally:
            session.close()

    def delete_word(self, lemma: str) -> bool:
        session = self.get_session()
        try:
            word = session.query(Word).filter_by(lemma=lemma).first()
            if word:
                # Удаляем все связанные словосочетания полностью
                for colloc in word.collocations[:]:
                    session.delete(colloc)
                session.delete(word)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def delete_collocation(self, phrase: str) -> bool:
        session = self.get_session()
        try:
            collocation = session.query(Collocation).filter_by(phrase=phrase).first()
            if collocation:
                session.delete(collocation)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def clear_all_dictionary(self) -> tuple[int, int]:
        session = self.get_session()
        try:
            word_count = session.query(Word).count()
            collocation_count = session.query(Collocation).count()

            session.query(Collocation).delete()
            session.query(Word).delete()

            session.commit()
            return (word_count, collocation_count)
        finally:
            session.close()

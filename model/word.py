from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from config.db import Base


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    word: Mapped[str] = mapped_column(unique=True, index=True)
    definition: Mapped[str]
    user_id: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    is_learned: Mapped[bool] = mapped_column(default=False)  # status of the word
    cards: Mapped[bool] = mapped_column(default=False)
    word_translation: Mapped[bool] = mapped_column(default=False)
    constructor: Mapped[bool] = mapped_column(default=False)
    word_audio: Mapped[bool] = mapped_column(default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "word": self.word,
            "definition": self.definition,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "is_learned": self.is_learned,
            "cards": self.cards,
            "word_translation": self.word_translation,
            "constructor": self.constructor,
            "word_audio": self.word_audio,
        }

    def __repr__(self):
        return f"""<Word(id={self.id}, word={self.word}, definition={self.definition}, 
        user_id={self.user_id}, created_at={self.created_at}, 
        is_learned={self.is_learned}, cards={self.cards}, word_translation={self.word_translation}
        , constructor={self.constructor}, word_audio={self.word_audio})>"""

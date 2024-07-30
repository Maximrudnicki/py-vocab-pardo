from config.db import SessionLocal

from model.word import Word


class WordRepository:
    def get_db(self):
        db = SessionLocal()
        try:
            return db
        finally:
            db.close()

    def add(self, word: Word) -> int:
        with self.get_db() as db:
            db.add(word)
            db.commit()
            db.refresh(word)
            return word.id

    def save(self, word: Word) -> None:
        with self.get_db() as db:
            db.add(word)
            db.commit()

    def update(self, word_id: int, updated_word: Word) -> None:
        with self.get_db() as db:
            word = db.query(Word).filter(Word.id == word_id).first()
            for key, value in updated_word.to_dict().items():
                if value is not None:
                    setattr(word, key, value)
            db.commit()

    def update_status(self, word_id: int, is_learned: bool) -> None:
        with self.get_db() as db:
            word = db.query(Word).filter(Word.id == word_id).first()
            word.is_learned = is_learned
            db.commit()

    def delete(self, word_id: int) -> None:
        with self.get_db() as db:
            word = db.query(Word).filter(Word.id == word_id).first()
            db.delete(word)
            db.commit()

    def find_by_user_id(self, user_id: int) -> list[Word]:
        with self.get_db() as db:
            return db.query(Word).filter(Word.user_id == user_id).all()

    def find_by_id(self, word_id: int) -> Word:
        with self.get_db() as db:
            return db.query(Word).filter(Word.id == word_id).first()

    def manage_trainings(self, word_id: int, training: str, res: bool) -> None:
        with self.get_db() as db:
            word = db.query(Word).filter(Word.id == word_id).first()

            if training == "cards":
                word.cards = res
            elif training == "word_translation":
                word.word_translation = res
            elif training == "constructor":
                word.constructor = res
            elif training == "word_audio":
                word.word_audio = res
            else:
                raise ValueError("Unknown training")

            word.is_learned = (
                word.cards
                and word.word_translation
                and word.constructor
                and word.word_audio
            )

            db.commit()

    def is_owner_of_word(self, user_id: int, word_id: int) -> bool:
        with self.get_db() as db:
            word = db.query(Word).filter(Word.id == word_id).first()
            return word is not None and word.user_id == user_id

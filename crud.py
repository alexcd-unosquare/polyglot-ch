from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func, select

import models
import schemas


def get_lang(db: Session, lang_id: int):
    return db.query(models.Lang).filter(models.Lang.id == lang_id).first()


def get_lang_by_name(db: Session, name: str):
    return db.query(models.Lang).filter(models.Lang.name == name).first()


def get_all_lang(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lang).offset(skip).limit(limit).all()


def add_lang(db: Session, name: str):
    db_lang = models.Lang(name=name)
    db.add(db_lang)
    db.commit()
    db.refresh(db_lang)
    return db_lang


def get_words(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Word).offset(skip).limit(limit).all()


def get_random_words(db: Session, limit: int):
    db_words = db.query(models.Word).order_by(func.random())
    return [db_words.first() for _ in range(limit)]


def create_lang_word(db: Session, word: schemas.WordCreate, lang_id: int):
    db_word = models.Word(**word.dict(), lang_id=lang_id)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


def add_words(db: Session, words: List[dict], lang_id: int):
    db_words = [models.Word(**word, lang_id=lang_id) for word in words]
    db.add(db_words)
    db.commit()
    db.refresh(db_words)
    return db_words


def get_word_by_id(db: Session, word_id: int):
    return db.query(models.Word).filter(models.Word.id == word_id).first()


def get_random_words_by_lang(db: Session, lang_id: int, limit: int):
    db_words = db.query(models.Word).order_by(func.random()).filter(models.Word.lang_id == lang_id)
    return [db_words.first() for _ in range(limit)]


def update_lang(db: Session, lang_id: int, new_lang: schemas.LangCreate):
    lang = db.query(models.Lang).get(lang_id)
    lang.name = new_lang.name
    db.commit()
    db.refresh(lang)
    return lang


def update_word(db: Session, word_id: int):
    word = db.query(models.Word).get(word_id)

    db.commit()
    db.refresh(word)
    return word


def get_learned(db: Session):
    return db.query(models.Word).filter(models.Word.learned is True).all()


def delete_word(db: Session, word_id: int):
    word = db.query(models.Word).filter(models.Word.id == word_id).first()
    db.delete(word)
    db.commit()
    return word


def delete_lang(db: Session, lang_id: int):
    lang = db.query(models.Lang).filter(models.Lang.id == lang_id).first()
    db.delete(lang)
    db.commit()
    return lang

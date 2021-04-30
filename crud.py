from typing import List
from helper import get_words_from_file, get_def
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


def create_lang(db: Session, name: str):
    db_lang = models.Lang(name=name)
    db.add(db_lang)
    db.commit()
    db.refresh(db_lang)
    db_lang = get_lang_by_name(db, name)
    words = get_words_from_file(name)
    add_words(db, words, db_lang.id)
    return db_lang


def get_words(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Word).offset(skip).limit(limit).all()


def get_random_words(db: Session, limit=20):
    order = select.order_by(func.random())
    return db.query(models.Word).order_by(order).limit(limit).all()


def create_lang_word(db: Session, word: schemas.WordCreate, lang_id: int):
    db_word = models.Word(**word.dict(), lang_id=lang_id)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


def add_words(db: Session, words: List[schemas.WordCreate], lang_id: int):
    db_words = [models.Word(**word.dict(), lang_id=lang_id) for word in words]
    db.add(db_words)
    db.commit()
    db.refresh(db_words)
    return db_words


def get_word_by_id(db: Session, word_id: int):
    return db.query(models.Word).filter(models.Word.id == word_id).first()
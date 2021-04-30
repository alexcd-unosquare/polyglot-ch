from typing import List

from fastapi import Depends, FastAPI, HTTPException, File
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/new/")
def create_new_lang(lang: schemas.LangCreate, db: Session = Depends(get_db)):
    db_lang = crud.get_lang_by_name(db, lang.name)

    if db_lang:
        raise HTTPException(status_code=400, detail="Language already exist")
    return crud.create_lang(db, 'en_US')


@app.get("/langs/", response_model=List[schemas.Lang])
def read_langs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    langs = crud.get_all_lang(db, skip=skip, limit=limit)
    return langs


@app.get("/langs/{lang_id}", response_model=schemas.Lang)
def read_lang(lang_id: int, db: Session = Depends(get_db)):
    db_lang = crud.get_lang(db, lang_id=lang_id)
    if db_lang is None:
        raise HTTPException(status_code=404, detail="Language not found")
    return db_lang


@app.post("/langs/{lang_id}/add/", response_model=schemas.Word)
def create_word_for_lang(
    lang_id: int, word: schemas.WordCreate, db: Session = Depends(get_db)
):
    return crud.create_lang_word(db=db, word=word, lang_id=lang_id)


@app.get("/words/", response_model=List[schemas.Word])
def read_words(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    words = crud.get_words(db, skip=skip, limit=limit)
    return words


'''
@app.get('/words/{lang}')
def get_random(lang: str, num: Optional[int] = 15):
    return 
'''
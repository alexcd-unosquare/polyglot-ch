from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Languages",
        "description": "Manage the supported languages.",
    },
    {
        "name": "Words",
        "description": "Add, update or delete words.",
    },
    {
        "name": "Random",
        "description": "Get randomized words by language or in general"
    }
]


app = FastAPI(title="Polyglot Challenge", openapi_tags=tags_metadata)

'''
origins = [
    "https://polyglot-challenge.herokuapp.com",
    "127.0.0.1:8000",
    "0.0.0.0",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def hello():
    return "https://polyglot-challenge.herokuapp.com/docs"


@app.get("/langs/", response_model=List[schemas.Lang], tags=['Languages'])
def get_all_langs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_lang(db, skip=skip, limit=limit)


@app.get("/langs/{lang_id}/", response_model=schemas.Lang, tags=['Languages'])
def get_lang_by_id(lang_id: int, db: Session = Depends(get_db)):
    db_lang = crud.get_lang(db, lang_id=lang_id)
    if db_lang is None:
        raise HTTPException(status_code=404, detail="Language not found")
    return db_lang


@app.post("/langs/add", response_model=schemas.Lang, tags=['Languages'])
def add_lang(lang: schemas.LangCreate, db: Session = Depends(get_db)):
    db_lang = crud.get_lang_by_name(db, lang.name)
    if db_lang:
        raise HTTPException(status_code=400, detail="Language already exist")
    return crud.add_lang(db, lang.name)


@app.put("/langs/{lang_id}/", response_model=schemas.Lang, tags=['Languages'])
def replace_lang(lang_id: int, new_lang: schemas.LangCreate, db: Session = Depends(get_db)):
    return crud.update_lang(db, lang_id, new_lang)


@app.delete("/langs/{lang_id}", response_model=models.Lang, tags=['Language'])
def delete_word(lang_id, db: Session = Depends(get_db)):
    return crud.delete_lang(db, lang_id)


@app.post("/langs/{lang_id}/add", response_model=schemas.Word, tags=['Words'])
def add_word_to_lang(lang_id: int, word: schemas.WordCreate, db: Session = Depends(get_db)):
    return crud.create_lang_word(db=db, word=word, lang_id=lang_id)


@app.get("/words/{word_id}", response_model=schemas.Word, tags=['Words'])
def get_word(word_id: int, db: Session = Depends(get_db)):
    return crud.get_word_by_id(db, word_id)


@app.get("/learned/", response_model=List[schemas.Word], tags=['Words'])
def get_learned_words(db: Session = Depends(get_db)):
    return crud.get_learned(db)


@app.get("/random/{lang_id}/", response_model=List[schemas.Word], tags=['Random'])
def get_random_by_lang(lang_id: int, db: Session = Depends(get_db), limit=20):
    return crud.get_random_words_by_lang(db, lang_id, limit)


@app.get("/random/", response_model=List[schemas.Word], tags=['Random'])
def get_random_words(db: Session = Depends(get_db), limit=20):
    return crud.get_random_words(db, limit)


@app.get("/words/", response_model=List[schemas.Word], tags=['Words'])
def get_all_words(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    words = crud.get_words(db, skip=skip, limit=limit)
    return words


@app.put("/words/{word_id}/", response_model=models.Word, tags=['Words'])
def mark_as_learned(word_id: int, db: Session = Depends(get_db)):
    return crud.update_word(db, word_id)


@app.delete("/words/{word_id}", response_model=models.Word, tags=['Word'])
def delete_word(word_id, db: Session = Depends(get_db)):
    return crud.delete_word(db, word_id)



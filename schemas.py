from typing import List, Optional

from pydantic import BaseModel


class WordBase(BaseModel):
    name: str
    definition: str
    example: str
    learned: bool
    times_seen: int


class WordCreate(WordBase):
    pass


class Word(WordBase):
    id: int
    lang_id: int

    class Config:
        orm_mode = True


class LangBase(BaseModel):
    name: str


class LangCreate(LangBase):
    pass


class Lang(LangBase):
    id: int
    words: List[Word] = []

    class Config:
        orm_mode = True

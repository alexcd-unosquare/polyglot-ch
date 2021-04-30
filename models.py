from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Lang(Base):
    __tablename__ = 'langs'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    words = relationship('Word', back_populates='lang')


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    definition = Column(String(255))
    example = Column(String(255))
    learned = Column(Boolean)
    times_seen = Column(Integer)
    lang_id = Column(Integer, ForeignKey('langs.id'))
    lang = relationship('Lang', back_populates='words')


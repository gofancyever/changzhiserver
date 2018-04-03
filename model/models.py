from sqlalchemy import Column, String, DateTime, Text,Integer,ForeignKey,Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from model.config import engine
Base = declarative_base()
class ChangzhiServerSection(Base):
    __tablename__ = 'ChangzhiServerSection'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    url = Column(Text)
    pages = relationship('ChangzhiServerPage')
    runningDate = Column(DateTime)


class ChangzhiServerPage(Base):
    __tablename__ = 'ChangzhiServerPage'
    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey('ChangzhiServerSection.id'))
    title = Column(Text)
    url = Column(Text)
    content = Column(Text)
    runningDate = Column(DateTime)


class ChangzhiServerNewsModel(Base):
    __tablename__ = 'ChangzhiServerNews'
    id = Column(Integer, primary_key=True)
    section = Column(Text)
    title = Column(Text)
    date = Column(DateTime)
    url = Column(Text)
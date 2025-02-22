from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from leetcode_execution_api.db.base import Base


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)

    tests = relationship(
        "Test",
        backref="question",
        cascade="all, delete-orphan",)

class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    question_id = Column(Integer, ForeignKey("question.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

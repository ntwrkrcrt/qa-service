from datetime import datetime

from pydantic import BaseModel


class Question(BaseModel):
    id: int
    text: str
    created_at: datetime


class Answer(BaseModel):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime


class QuestionWithAnswers(Question):
    answers: list[Answer] = []

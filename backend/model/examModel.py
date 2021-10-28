from typing import List, Optional
from odmantic import ObjectId
from pydantic import BaseModel, Field
from odmantic.bson import BaseBSONModel


class Candidate(BaseModel):
    matric_no: str = Field(max_length=20)
    password: bytes = Field(min_length=3)
    phone: str = Field(max_length=15)
    score: Optional[int] = 0
    done: bool = False

    class Config:
        anystr_lower = True


class Score(BaseModel):
    score: int
    candidateId: str


class Question(BaseModel):
    question: str
    option1: str
    option2: str
    option3: Optional[str]
    option4: Optional[str]
    answer: str

    class Config:
        anystr_lower = True


class ExamModel(BaseModel):
    questions: List[Question]
    candidates: List[Candidate]
    duration: int
    title: str

    class Config:
        anystr_lower = True


class ExamResponseModel(BaseBSONModel):
    id: ObjectId
    duration: int
    title: str
    question: List[Question]


class CandidateLogin(BaseModel):
    matric_no: str
    password: str

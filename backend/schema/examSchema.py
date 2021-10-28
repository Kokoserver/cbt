from typing import List, Optional
from odmantic import Model, Reference, EmbeddedModel, Field

from .userSchema import User


class Question(EmbeddedModel):
    question: str
    option1: str
    option2: str
    option3: Optional[str]
    option4: Optional[str] = ""
    answer: str


class Candidate(EmbeddedModel):
    matric_no: str
    password: str
    phone:str
    score: int = 0
    done: bool = False


class Exam(Model):
    question: List[Question]
    candidate: List[Candidate]
    duration: int = 20
    title: str
    user: User = Reference()

    # @property
    # async def get_question(self):
    #     return self.question

    # @property
    # async def get_candidate(self):
    #     return self.candidate

    # @property
    # async def get_duration(self):
    #     return self.duration

    # @property
    # async def get_user(self):
    #     return self.user

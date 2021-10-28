from typing import List
from odmantic.bson import ObjectId
from repository.general_enums import LevelChoice, SemesterChoice
from pydantic import BaseModel
from repository.general_enums import DepartmentEnum
class QuestionUpdate(BaseModel):
    question:str
    options:List[str] = []
    answer:str
    semester:SemesterChoice = SemesterChoice.first_semester
    level:LevelChoice = LevelChoice.hundred
    department:DepartmentEnum = DepartmentEnum.computer_science

class Question(BaseModel):
    question:str
    options:List[str] = []
    answer:str
    semester:SemesterChoice = SemesterChoice.first_semester
    level:LevelChoice = LevelChoice.hundred
    department:DepartmentEnum = DepartmentEnum.computer_science

class SaveQuestion(Question):
    id:ObjectId

class QuestionResponseModel(Question):
    id:str
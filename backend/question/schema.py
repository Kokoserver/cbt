from typing import List
from odmantic import Model
from repository.general_enums import DepartmentEnum
from repository.general_enums import  LevelChoice, SemesterChoice


class Question(Model):
    question:str
    options:List[str] = []
    answer:str
    semester:SemesterChoice
    level:LevelChoice
    department:DepartmentEnum

from odmantic.bson import ObjectId
from pydantic import BaseModel
from backend.question.model import DepartmentEnum
from repository.general_enums import  LevelChoice, SemesterChoice


class Exam(BaseModel):
    semaster: SemesterChoice = SemesterChoice.first_semester
    level: LevelChoice = LevelChoice.hundred
    department: DepartmentEnum = DepartmentEnum.computer_science



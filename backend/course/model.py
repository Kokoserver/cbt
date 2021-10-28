from odmantic.bson import ObjectId
from pydantic import BaseModel
from backend.question.model import DepartmentEnum
from repository.general_enums import CourseExamDuration, CourseUnitChoice, LevelChoice, SemesterChoice


class CourseUpdate(BaseModel):
    code: str
    title: str
    unit:CourseUnitChoice = CourseUnitChoice.one
    semaster: SemesterChoice = SemesterChoice.first_semester
    level: LevelChoice = LevelChoice.hundred
    department: DepartmentEnum = DepartmentEnum.computer_science
    duration:CourseExamDuration = CourseExamDuration.fiften_minutes 

class SaveCourse(CourseUpdate):
    id:ObjectId



class Course(BaseModel):
    code: str
    title: str
    unit:CourseUnitChoice = CourseUnitChoice.one
    semaster: SemesterChoice = SemesterChoice.first_semester
    level: LevelChoice = LevelChoice.hundred
    department:DepartmentEnum = DepartmentEnum.computer_science
    duration:CourseExamDuration = CourseExamDuration.fiften_minutes


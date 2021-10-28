from typing import AnyStr
from odmantic import Model
from backend.course.model import DepartmentEnum
from repository.general_enums import  CourseExamDuration, LevelChoice, SemesterChoice


class Course(Model):
    code: str
    title: str
    unit: int
    semester: SemesterChoice = SemesterChoice.first_semester
    level: LevelChoice = LevelChoice.hundred
    department: DepartmentEnum
    duration:CourseExamDuration = CourseExamDuration.fiften_minutes



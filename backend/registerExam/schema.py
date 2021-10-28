from typing import AnyStr
from odmantic import Model, Reference
from repository.general_enums import DepartmentEnum
from repository.general_enums import  CourseExamDuration, LevelChoice, SemesterChoice


class Course(Model):
    code: str
    title: str
    unit: int
    semester: SemesterChoice = SemesterChoice.first_semester
    level: LevelChoice = LevelChoice.hundred
    department: DepartmentEnum
    duration:CourseExamDuration = CourseExamDuration.fiften_minutes



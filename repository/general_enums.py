from enum import Enum, IntEnum
class DepartmentEnum(str, Enum):
    computer_science = "computer science"
    mass_communication = "mass communication"
    lis = "LIS"
    acccounting = "accounting"
    actuarial_Science = "actuarial Science"
    agricultural_engineering = "agricultural Engineering"
    agriculture = "agriculture"
    arabic_Studies = "arabic Studies"
    biochemistry =  "biochemistry"
    business_administration = "business administration"


class SemesterChoice(str, Enum):
    first_semester = "rain"
    second_semster = "harmattan"

class CourseUnitChoice(IntEnum):
    one = 1
    two= 2
    three = 3
    four = 4
    six = 6


class ExamDuration(IntEnum):
    five = 5
    ten_minutes = 10
    fiften_minutes = 15
    tweenty_minutes = 20
    twentifive_minutes = 25
    thirty_minutes = 30
    thirtifive_minutes = 35
    fourty_minutes = 40
    fourtfive_minutes = 45
    fifty_minutes = 50
    fiftyfive_minutes = 55
    one_hour = 60


class LevelChoice(IntEnum):
    hundred = 100
    two_hundred = 200
    three_hundred = 300
    four_hundred = 400

department_list:list = [deppartment for deppartment in dir(DepartmentEnum) if not deppartment.startswith('_')]
level_list:list = [level for level in dir(LevelChoice) if not level.startswith('_')]
semester_list:list = [semester for semester in dir(SemesterChoice) if not semester.startswith('_')]
unit_list:list = [unit for unit in dir(CourseUnitChoice) if not unit.startswith('_')]
duration_list:list = [duration for duration in dir(ExamDuration) if not duration.startswith('_')]

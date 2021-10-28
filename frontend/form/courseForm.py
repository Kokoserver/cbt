from pydantic.utils import Obj
from repository.general_enums import *
from typing import  Optional
from fastapi.requests import Request


class UpdateCourseForm:
     def __init__(self, request:Request) -> None:
          self.request = request
          self.errors:dict = {}
          self.title:Optional[str] = None
          self.unit:Optional[CourseUnitChoice] = None
          self.semaster:Optional[SemesterChoice] = None
          self.level:Optional[LevelChoice] = None
          self.department:Optional[DepartmentEnum] = None
          self.id:object = None
          self.duration:Optional[CourseExamDuration] = None

     async def load(self):
          form = await self.request.form()
          self.title = form.get("title")
          self.unit = form.get("unit")
          self.semaster = form.get("semaster")
          self.level = form.get("level")
          self.department = form.get("department")
          self.duration = form.get("duration")
          self.id = object(form.get("id"))

     async def is_valid(self):
          if self.level != level_list:
                self.errors.update({"level":"level is invalid"}) 
                
          if not self.semaster in semester_list:
               self.errors.update({"semaster":"Invalid department semaster"}) 

          if not self.unit in unit_list:
               self.errors.update({"unit":"Invalid  unit"}) 

          if not self.department in semester_list:
               self.errors.update({"department":"Invalid department"}) 
          if not self.errors:
               return True
          return False   

class RegisterForm:
     def __init__(self, request:Request) -> None:
          self.request = request
          self.errors:dict = {}
          self.title:Optional[str] = None
          self.unit:Optional[CourseUnitChoice] = None
          self.semaster:Optional[SemesterChoice] = None
          self.level:Optional[LevelChoice] = None
          self.department:Optional[DepartmentEnum] = None
          self.duration:Optional[CourseExamDuration] = None

     async def load(self):
          form = await self.request.form()
          self.title = form.get("title")
          self.unit = form.get("unit")
          self.semaster = form.get("semaster")
          self.level = form.get("level")
          self.department = form.get("department")
          self.duration = form.get("duration")

     async def is_valid(self):
          if self.level != level_list:
                self.errors.update({"level":"level is invalid"}) 
                
          if not self.semaster in semester_list:
               self.errors.update({"semaster":"Invalid department semaster"}) 

          if not self.unit in unit_list:
               self.errors.update({"unit":"Invalid  unit"}) 

          if not self.department in semester_list:
               self.errors.update({"department":"Invalid department"}) 
          if not self.errors:
               return True
          return False        


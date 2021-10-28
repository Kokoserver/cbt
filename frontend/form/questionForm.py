from typing import  Optional
from fastapi.requests import Request
from repository.general_enums import *

class UpdateQuestionForm:
     def __init__(self, request:Request) -> None:
          self.request = request
          self.errors:dict = {}
          self.options1:Optional[str] = None
          self.options2:Optional[str] = None
          self.options3:Optional[str] = None
          self.options4:Optional[str] = None
          self.answer:Optional[str] = None
          self.semester:Optional[SemesterChoice] = None
          self.level:Optional[LevelChoice] = None
          self.id:Optional[str] = None
          self.department:Optional[DepartmentEnum] = None


     async def load(self):
          form = await self.request.form()
          self.question:str = form.get("question")
          self.options1:Optional[str] = form.get("option1")
          self.options2:Optional[str] = form.get("option2")
          self.options3:Optional[str] = form.get("option3")
          self.options4:Optional[str] = form.get("option3")
          self.answer :str= form.get("answer")
          self.semester:SemesterChoice = form.get("semester")
          self.level:LevelChoice = form.get("level")
          self.id:object = object(form.get("id"))
          

     async def is_valid(self):
          if self.level not in  level_list:
                self.errors.update({"level":"please specify the level that will take this question"}) 
          if not self.semester not in semester_list:
               self.errors.update({"semester":"please specify the semester"}) 
          if not self.semester not in department_list:
               self.errors.update({"semester":"please specify the semester"}) 
          if not self.answer != self.options1 or self.options2 or self.options3 or self.options4:
               self.errors.update({"options":"answer must be part the options"})
          if not len(self.question)  > 3:
               self.errors.update({"question":"question must be greater than 3 character"})
          if not self.errors:
               return True
          return False
        

class AddQuestionForm:
     def __init__(self, request:Request) -> None:
          self.request = request
          self.errors:dict = {}
          self.options1:Optional[str] = None
          self.options2:Optional[str] = None
          self.options3:Optional[str] = None
          self.options4:Optional[str] = None
          self.answer:Optional[str] = None
          self.semester:Optional[SemesterChoice] = None
          self.level:Optional[LevelChoice] = None
          self.department:Optional[DepartmentEnum] = None

     async def load(self):
          form = await self.request.form()
          self.question:str = form.get("question")
          self.options1:Optional[str] = form.get("option1")
          self.options2:Optional[str] = form.get("option2")
          self.options3:Optional[str] = form.get("option3")
          self.options4:Optional[str] = form.get("option3")
          self.answer :str= form.get("answer")
          self.semester:SemesterChoice = form.get("semester")
          self.level:LevelChoice = form.get("level")

     async def is_valid(self):
          if self.level not in  level_list:
               self.errors.update({"level":"please specify the level that will take this question"}) 
          if not self.semester not in semester_list:
               self.errors.update({"semester":"please specify the semester"}) 
          if not self.semester not in department_list:
               self.errors.update({"semester":"please specify the semester"}) 
          if not self.answer != self.options1 or self.options2 or self.options3 or self.options4:
               self.errors.update({"options":"answer must be part the options"})
          if not len(self.question)  > 3:
               self.errors.update({"question":"question must be greater than 3 character"})
          if not self.errors:
               return True
          return False
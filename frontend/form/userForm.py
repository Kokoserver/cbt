from typing import  Optional
from fastapi.requests import Request



class UpdateForm:
     def __init__(self, request:Request) -> None:
          self.request = request
          self.errors:dict = {}
          self.firstname:Optional[str] = None
          self.lastname:Optional[str] = None
          self.email:Optional[str] = None
          self.password:Optional[bytes] = None
          self.id:Optional[bytes] = None
          self.confrimPassword:Optional[bytes] = None

     async def load(self):
          form = await self.request.form()
          self.firstname:str = form.get("firstname")
          self.lastname :str= form.get("lastname")
          self.email:str = form.get("email")
          self.phone:str = form.get("phone")
          self.password:bytes = form.get("password")
          self.id:bytes = form.get("id")
          self.confirmPassword:bytes =  form.get("confirmPassword")

     async def is_valid(self):
          if self.password != self.confirmPassword:
                self.errors.update({"confirmPassword":"password do not match"}) 
          if not self.email.find("@"):
               self.errors.update({"email":"Invalid email address"}) 
          if not len(self.firstname) and len(self.lastname) and len(self.email) and len(self.phone) > 3:
               self.errors = {
               "firstname":"firstname must be greater than 3 character",
               "lastname":"firstname must be greater than 3 character",
               "email":"email must be greater than 3 character",
               "phone":"phone number must be greater than 3 character",
          }
          if not self.errors:
               return True
          return False
        

class RegisterForm:
     def __init__(self, request:Request) -> None:
          self.request = request
          self.errors:dict = {}
          self.firstname:Optional[str] = None
          self.lastname:Optional[str] = None
          self.email:Optional[str] = None
          self.password:Optional[bytes] = None
          self.confrimPassword:Optional[bytes] = None

     async def load(self):
          form = await self.request.form()
          self.firstname:str = form.get("firstname")
          self.lastname :str= form.get("lastname")
          self.email:str = form.get("email")
          self.phone:str = form.get("phone")
          self.password:bytes = form.get("password")
          self.confirmPassword:bytes =  form.get("confirmPassword")

     async def is_valid(self):
          if self.password != self.confirmPassword:
                self.errors.update({"confirmPassword":"password do not match"}) 
          if not self.email.find("@"):
               self.errors.update({"email":"Invalid email address"}) 
          if not len(self.firstname) and len(self.lastname) and len(self.email) and len(self.phone) > 3:
               self.errors = {
               "firstname":"firstname must be greater than 3 character",
               "lastname":"firstname must be greater than 3 character",
               "email":"email must be greater than 3 character",
               "phone":"phone number must be greater than 3 character",
          }
          if not self.errors:
               return True
          return False        

class LoginForm:
     def __init__(self, request:Request) -> None:
          self.request = request
          self.errors:dict = {}
          self.email:Optional[str] = None
          self.password:Optional[bytes] = None
          self.username:Optional[str] = None


     async def load(self):
          form = await self.request.form()
          self.email:str = form.get("email")
          self.password:bytes = form.get("password")
          self.username = self.email


     async def is_valid(self):
          if not self.email.find("@"):
               self.errors.update({"email":"Invalid email address"}) 
          if not self.password:
               self.errors.update({"password":"password is required"})
          if not self.errors:
               return True
          return False
        
               








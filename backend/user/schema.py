from os import urandom
from datetime import date, datetime
from typing import Optional
from odmantic import Model, Field
from pydantic import EmailStr

exam_number = f" {date.today().year}/{urandom(5).hex()}"

class User(Model):
    exam_No:Optional[str]= Field(default=exam_number)
    firstname: str = Field(min_length=3)
    lastname: str = Field(min_length=3)
    email: EmailStr = Field()
    phone: str = Field(max_length=14)
    password: bytes
    is_active: bool = False
    is_admin: bool = False
    created_at: Optional[datetime] = datetime.now()


    



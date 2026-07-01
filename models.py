from typing import Optional
from pydantic import BaseModel,Field, EmailStr


# class User(BaseModel):
#     age: int
#     name: str
class User(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    age: int | None
    is_subscribed: bool  | None

class Contact(BaseModel):
    email: EmailStr
    phone: str | None = Field(
        default=None,
        pattern=r"^\d+$", min_length=7, max_length=15) 
    
class Feedback(BaseModel):
    message: str = Field(min_length=10, max_length=500)
    name: str = Field(min_length=2, max_length=50)
    contact: Contact

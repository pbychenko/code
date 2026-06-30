from pydantic import BaseModel,Field, EmailStr


class User(BaseModel):
    age: int
    name: str

class Contact(BaseModel):
    email: EmailStr
    phone: int = Field(..., gt=0, lt=10000000000)  # Example: phone number must be a positive integer less than 10 billion
    
class Feedback(BaseModel):
    message: str = Field(min_length=10, max_length=500)
    name: str = Field(min_length=2, max_length=50)
    # contact: Contact

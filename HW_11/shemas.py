from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: str = Field(..., max_length=100)
    phone_number: str = Field(..., max_length=15)
    date_of_birth: date


class ContactCreate(ContactBase):
    done: bool


class ContactUpdate(ContactBase):
    done: bool


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True


class ContactListResponse(BaseModel):
    contacts: List[ContactResponse]


class UserAuthenticate(BaseModel):
    email: str
    password: str


# Модель для створення нового користувача
class UserCreate(BaseModel):
    email: str
    password: str
    avatar: Optional[str]

# Модель для JWT токена
class Token(BaseModel):
    access_token: str
    token_type: str

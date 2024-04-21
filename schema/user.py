from typing import Optional
from pydantic import BaseModel, EmailStr



class SignUpModel(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "password",
                "is_staff": False,
                "is_active": True,
            }
        }



class LoginModel(BaseModel):
    username: str
    password: str


class UpdateUserModel(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
            }
        }
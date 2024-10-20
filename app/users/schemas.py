import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class SUserRegister(BaseModel):
    fio: str = Field(..., min_length=3, max_length=50, description="ФИО")
    username: str = Field(..., min_length=5, max_length=15, description="Имя пользователя")
    password: str = Field(..., min_length=5, max_length=15, description="Пароль, от 5 до 15 знаков")


class SUserAuth(BaseModel):
    username: str = Field(..., min_length=5, max_length=15, description="Имя пользователя")
    password: str = Field(..., min_length=5, max_length=15, description="Пароль, от 5 до 15 знаков")
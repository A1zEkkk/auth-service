from pydantic import BaseModel, Field, field_validator, EmailStr
from schemas.utils import normalize_phone_number
from core.exc.validation import InvalidSymbolError, InvalidLengthError

class AuthRequestsUsingPhone(BaseModel):
    phone: str
    password: str

    @field_validator("phone", mode="before")
    @classmethod
    def phone_validator(cls, value):
        return normalize_phone_number(value)

    @field_validator("password", mode="before")
    @classmethod
    def get_hash_for_password(cls, v):
        if not (8 <= len(v) <= 50):
            raise InvalidSymbolError

        upper = lower = digit = False

        for i in v:
            if i.isupper():
                upper = True
            if i.islower():
                lower = True
            if i.isdigit():
                digit = True

        if not (upper and lower and digit):
            raise InvalidSymbolError

        return v


class AuthRequestsUsingEmail(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password", mode="before")
    @classmethod
    def get_hash_for_password(cls, v):
        if not (8 <= len(v) <= 50):
            raise InvalidLengthError

        upper = lower = digit = False

        for i in v:
            if i.isupper():
                upper = True
            if i.islower():
                lower = True
            if i.isdigit():
                digit = True

        if not (upper and lower and digit):
            raise InvalidSymbolError

        return v
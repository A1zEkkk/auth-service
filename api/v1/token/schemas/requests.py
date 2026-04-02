from pydantic import BaseModel, EmailStr, model_validator, field_validator
from api.v1.user.utils import normalize_number
from core.configs import get_settings
from datetime import datetime

class TokenCreateSchema(BaseModel):
    id: int
    type_token: str
    email: EmailStr
    phone: str
    iat: int = datetime.now().timestamp()
    exp : int = None

    @model_validator(mode="after")
    def get_expire(self):
        if self.type_token == "access_token":
            self.exp = self.iat + get_settings().EXPIRE_AT_ACCESS
        else:
            self.exp = self.iat + get_settings().EXPIRE_AT_REFRESH

        return self


from pydantic import BaseModel, model_validator, Field
from typing_extensions import Self
import time
from core.configs import get_settings


class TokenData(BaseModel):
    type_token: str | None = None
    role: str
    user_id: int #когда должен перестать жить
    iat: int = Field(default_factory=lambda: int(time.time())) #Когда выпущен
    exp: int = None

    @model_validator(mode="after")
    def get_expire_for_class(self) -> Self:
        if self.type_token == "access_token":
            self.exp = self.iat + get_settings().EXPIRE_AT_ACCESS
            return self

        self.exp = self.iat + get_settings().EXPIRE_AT_REFRESH
        return self



token_access = TokenData(
    type_token="access_token",
    role="user",
    user_id=1,
)

token_refresh = TokenData(
    type_token="refresh_token",
    role="user",
    user_id=1,
)

print(token_access)
print(token_refresh)
from pydantic import BaseModel, EmailStr, model_validator, field_validator


def normalize_number(number: str) -> str:
    normalized_number = ""
    for i in number:
        if i not in "+-() ":
            normalized_number += i

    return normalized_number


class UserCreateSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    phone: str

    @model_validator(mode="after")
    def validate_data(self):
        if self.name == "" or self.surname == "":
            raise ValueError("Имя или фамииля не можети быть пустым")

        if len(self.password) < 8:
            raise ValueError("Пароль не может быть меньше 8 символов")

        for i in self.phone:
            if not i.isdigit() and i not in "+-() ":
                print("trace if", i)
                raise ValueError("Некорретно введенный номер")

        return self

    @model_validator(mode="after")
    def normalize_data(self):
        self.name = self.name.capitalize()
        self.surname = self.surname.capitalize()
        self.phone = normalize_number(self.phone)

        return self


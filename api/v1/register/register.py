from api.v1.schemas.dto.user import UserDTO
from api.v1.user.view import UserView, get_user_view
from api.v1.tokenJWT.service import TokenService, get_token_service
from api.v1.schemas.requests.user import UserCreate
from api.v1.schemas.requests.token_schema import TokenData

from fastapi import Depends

class RegisterUseCase:
    def __init__(self, user_view: UserView, token_service: TokenService):
        self.user_view = user_view
        self.token_service = token_service

    async def register_user(self, user: UserCreate):
        data = await self.user_view.create_user(user)

        user_dto = UserDTO.model_validate({
            "id": data.id,
            "name": data.name,
            "surname": data.surname,
            "email": data.email,
            "phone": data.phone,
            "role": data.role.name
        })

        token_data = TokenData(
            role=user_dto.role,
            user_id=user_dto.id
        )

        tokens = self.token_service.get_tokens(token_data)
        return tokens

def get_register_user(
        user_view: UserView = Depends(get_user_view),
        token_service: TokenService = Depends(get_token_service)
) -> RegisterUseCase:
    return RegisterUseCase(user_view, token_service)
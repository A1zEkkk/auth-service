from api.v1.schemas.dto.user import UserDTO
from api.v1.user.view import UserView
from api.v1.tokenJWT.service import TokenService
from api.v1.schemas.requests.user import UserCreate
from api.v1.schemas.requests.token import TokenData
from core.utils import hash_password

class RegisterUseCase:
    def __init__(self, user_view: UserView = UserView(), token_service: TokenService = TokenService()):
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

def get_register_user():
    return RegisterUseCase()
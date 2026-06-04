from schemas.dto.user import UserDTO
from api.v1.user.view import UserView, get_user_view
from service.jwt import TokenService, get_token_service
from schemas.user import UserCreate
from schemas.requests.token_schema import TokenData
from service.refresh import RefreshService, get_refresh_service
from core.rabbit.producer import RabbitProducer, get_rabbit_producer

from fastapi import Depends

class RegisterUseCase:
    def __init__(
            self,
            user_view: UserView,
            token_service: TokenService,
            refresh_service: RefreshService,
            producer: RabbitProducer
    ):
        self.user_view = user_view
        self.token_service = token_service
        self.refresh_service = refresh_service
        self.producer = producer

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

        tokens = await self.token_service.get_tokens(token_data)
        refresh_token = tokens['refresh_token']
        await self.refresh_service.insert_token(refresh_token)

        await self.producer.publish(
            queue_name="new_user",
            message=user_dto.model_dump()
        )



        return tokens

def get_register_user(
        user_view: UserView = Depends(get_user_view),
        token_service: TokenService = Depends(get_token_service),
        refresh_service: RefreshService = Depends(get_refresh_service),
        producer: RabbitProducer = Depends(get_rabbit_producer)
) -> RegisterUseCase:
    return RegisterUseCase(user_view, token_service, refresh_service, producer)
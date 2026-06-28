from fastapi import Depends

from core.exc.infrastructure.rabbit import NotificationDeliveryFailed
from services.user import UserService, get_user_service
from services.jwt import TokenService, get_token_service
from services.refresh import RefreshService, get_refresh_service
from services.producer import ProducerService, get_producer_service

from schemas.dto.user import UserDTO
from schemas.user import UserCreate
from schemas.JWT import TokenData

from outbox.repository import get_outbox_repository


class RegisterUseCase:
    def __init__(
            self,
            user_service: UserService,
            token_service: TokenService,
            refresh_service: RefreshService,
            producer_service: ProducerService
    ):
        self.user_service = user_service
        self.token_service = token_service
        self.refresh_service = refresh_service
        self.producer_service = producer_service

    async def register_user(self, user: UserCreate):
        data = await self.user_service.create_user(user)

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
        refresh_token = tokens['refresh_token']
        await self.refresh_service.insert_token(refresh_token)

        try:
            await self.producer_service.publish(
                queue_name="new_user",
                message=user_dto.model_dump()
            )
        except NotificationDeliveryFailed:
            print("Сработало исключение")
            repos = get_outbox_repository()
            await repos.create("new_user", user_dto.model_dump())

        return tokens

def get_register_user(
        user_service: UserService = Depends(get_user_service),
        token_service: TokenService = Depends(get_token_service),
        refresh_service: RefreshService = Depends(get_refresh_service),
        producer_service: ProducerService = Depends(get_producer_service)
) -> RegisterUseCase:
    return RegisterUseCase(user_service, token_service, refresh_service, producer_service)
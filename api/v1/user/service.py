from typing import Optional
from .repository import UserRepository

class UserService:

    def __init__(self, user_repository: UserRepository = UserRepository()):
        self.user_repository = user_repository

    def get_user_by_login(self, login):
        return self.user_repository.get_user_by_login(login)

    def get_user_by_phone(self, phone):
        return self.user_repository.get_user_by_phone(phone)


from typing import Optional
from core.db.db import database
from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload, lazyload, contains_eager


class TokenRepository:
    def __init__(self, db=database):
        self.db = db

    async def create_token(self):
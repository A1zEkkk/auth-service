import bcrypt
import hashlib

from core.configs import get_settings




def hash_password(password) -> bytes:
    settings = get_settings()
    return bcrypt.hashpw(
        password=password.encode(settings.ENCODING),
        salt=bcrypt.gensalt()
    )

def verify_hash_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

import bcrypt

from core.configs import get_settings




def hash_password(password) -> bytes:
    settings = get_settings()
    return bcrypt.hashpw(
        password=password.encode(settings.ENCODING),
        salt=bcrypt.gensalt()
    )

def verify_password(password, hashed_password) -> bool:
    settings = get_settings()
    return bcrypt.checkpw(
        password=password.encode(settings.ENCODING),
        hashed_password=hashed_password
    )
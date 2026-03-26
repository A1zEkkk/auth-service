from cfg import Settings

from authlib.jose import jwt
from time import time

import datetime


class Token:
    def __init__(self, settings: Settings):
        self.settings = settings


    def get_token(self, type_token: str, payload: dict):

        header = {"alg": self.settings.algorithm, "typ": type_token}
        payload["iat"] = int(time())

        token = jwt.encode(header, payload, self.settings.secret_key)
        return token

    def decode_token(self, token: str):
        claim = jwt.decode(token, self.settings.secret_key)
        type_token = claim["typ"]

        if type_token not in self.settings.secret_key:
            return 0


from_data = {}

try:
    name = from_data["name"]
except KeyError:
    print("error")
    raise
finally:
    print("finaly")
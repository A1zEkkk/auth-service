import os
from dotenv import load_dotenv

from authlib.jose import jwt


load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY') #HS256

print(SECRET_KEY)
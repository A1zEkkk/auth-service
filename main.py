from core.app import create_app
import time


#time.sleep(10)
# app = create_app()


from api.v1.tokenJWT.service import TokenService


token= TokenService()


jwt_token_access =       "eyJhbGciOiJIUzI1NiIsInR5cCI6ImFjY2Vzc190b2tlbiJ9.eyJpZCI6MjUsInJvbGUiOiJ1c2VyIiwiaWF0IjoxNzc3ODQzNjE2LCJleHAiOjE3Nzc4NDU0MTZ9._Oj61CvIjAc2pCGTNNRTUM6-t5lW6rWkmG9yHVNGU1I"
jwt_token_refresh =     "eyJhbGciOiJIUzI1NiIsI1R5cCI6InJlZnJlc2hfdG9rZW4ifQ.eyJpZCI6MjUsInJvbGUiOiJ1c2VyIiwiaWF0IjoxNzc3ODQzNjE2LCJleHAiOjE3ODA0NzMzNTl9.4GEkMNWO9tqolYkayEswcjeRjbJzalhjpEezxLH3f9w"



data_access = token.verify_token(jwt_token_access)
data_refresh = token.verify_token(jwt_token_refresh)

print(data_access)
print(data_refresh)
#Сделать исключение при декодировании токенов
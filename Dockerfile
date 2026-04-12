FROM python:3.13.13-alpine3.23
LABEL authors="None"
WORKDIR /src
COPY . .
RUN apk update && apk add --no-cache
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"]
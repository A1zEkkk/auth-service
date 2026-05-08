Быстрый запуск через билд докерфайла и общую сетку без. докеркомпоса
1) Создать общую сетку
docker network create my-network
2) Сбилдить образ
docker build -t auth-service .
3) Поднять постгрес контейнер
docker run -d --name postgres-db --network my-network -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 5432:5432 postgres:15-alpine
4) Поднять наш бекенд на основе образа
docker run -d --name my-app --network my-network -p 8000:8000 -e POSTGRES_HOST=postgres-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_PORT=5432 -e DB_NAME=postgres -e JWT_ALGORITHM=HS256 -e JWT_SECRET_KEY=kjgh809ph98fg679pfp99f7fyoil98ff78lg78pglo09ywac4a2bn auth-service

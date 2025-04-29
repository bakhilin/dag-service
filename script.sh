poetry run pytest --cov=app --cov-report=term-missing

sudo docker run -p 5432:5432 \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_USER=user \
    -e POSTGRES_DB=dbname  \
    postgres:13

curl -X GET "http://localhost:8080/api/graph/1/adjacency_list"

curl -X GET "http://localhost:8080/api/graph/1/reverse_adjacency_list"

curl -X GET "http://localhost:8080/api/graph/1"

curl -X DELETE "http://localhost:8080/api/graph/1/node/B"

export DATABASE_URL="sqlite+aiosqlite:///:memory:" # for testing in test env


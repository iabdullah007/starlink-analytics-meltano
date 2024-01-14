# install poetry & dependencies
init:
	poetry --version || brew install poetry \
	&& poetry install

# run docker-compose
up:
	cd starlink-analytics && docker-compose up 

# teardown docker-compose
down:
	cd starlink-analytics && docker-compose down

# rebuild the docker image
build:
	cd starlink-analytics && docker-compose build

query_data:
	docker exec -i meltano-system-db psql -U postgres -p postgres -d meltano -p 5432 -x < query.sql
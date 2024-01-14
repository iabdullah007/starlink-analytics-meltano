# Starlink Analytics

This is a Meltano project which extracts information from SpaceX-API, loads into Postgres DB and do analytics to find out
> When will there be 42,000 Starlink satellites in orbit, and how many launches will it take to get there?

## Requirements Development Env
- Docker
- Python v3.8
- Poetry (a python package manager)  



## Local Run & Development
- Install all dependencies - `poetry install`
- Install Meltano plugins - `poetry run meltano install`
- Run Postgres via Docker
```bash
$ docker run -d \
  -p 5438:5432 \
  --name meltano_postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=meltano \
  postgres:latest
```

- Expose environment variables for `tap_spacexapi`, Postgres loader `target-postgres` and dbt profile for `dbt-postgres`
```bash
$ echo "
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=meltano
" > .env

```

- Run extract and load pipeline which will get data form SpaceX-API and load to Postgres DB
```bash
poetry run meltano elt tap-spacexapi target-postgres
```

- Run transformation job to do the analytics via dbt. A table named `meltano.analytics.starlink_launches` will appear in Postgres DB.
```bash
poetry run meltano invoke dbt-postgres:run
```

- You can connect your SQL Client to the Postgres DB with credentials above to see the data.
- You can also run below statement
```bash
docker exec -i meltano_postgres psql -U postgres -p postgres -d meltano -p 5432 -x <<EOF
SELECT * FROM analytics.starlink_launches;
EOF
```

## Teardown
- Kill the Postgres and remove the container
```bash
docker kill $(docker ps | grep "meltano_postgres" | awk '{print $1}')
```

## Useful Resources

* [Meltano Official Website](https://meltano.com/)
* [Meltano Docs](https://docs.meltano.com/)
* [Meltano Tutorial: Create a Custom Extractor](https://docs.meltano.com/tutorials/custom-extractor)
* [Meltano target-postgres Docs](https://hub.meltano.com/loaders/target-postgres/)
* [SpaceX-API Docs](https://github.com/r-spacex/SpaceX-API/blob/master/docs/README.md)
* [dbt Docs](https://docs.getdbt.com/)
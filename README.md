# FastAPI + SQLModel + Dash

Sample project that uses SQLModel, Postgres, FastAPI, dash, and Docker.

## Setting up the project

All services are containarized and hadled by docker compose.
There is a starter script for populating the database with fake data.
Setup up the project as follows:

```bash
docker-compose up -d --build
docker-compose exec api python -m app.faker
```

The second command is only necessary the first time you run to populate the DB.
Afterwards, docker compose persits the DB data into the local disk.

The postgress DB can be accessed outside the container at the following address:
`postgresql://root:root@localhost:5432/sales`

### Stop and erase data
If you want to start from scratch, stop containers and remove volumes with:

```bash
docker-compose down -v
```

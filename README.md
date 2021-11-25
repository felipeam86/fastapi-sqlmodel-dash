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

### Stop and erase data
If you want to start from scratch, stop containers and remove volumes with:

```bash
docker-compose down -v
```

## Overview of the project

The project consists of the following pieces:

- Rest API built with FastAPI for accessing the data.
- The data models are created with SQLmodel.
- A postgresql database. The project has a script to populate the database with fake data. It can be used as indicated above. It is found on `api/app/faker.py`.
- A visualization dashboard built with Plotly Dash
- a PGadmin service for accessing and doing maintenance on the postgres DB.


## Rest API

The rest API is accessible on http://127.0.0.1:8000/. All endpoints are properly documented on:

http://127.0.0.1:8000/docs

You can also test the endpoints from within the documentation.

![Rest API docs](screenshots/api_docs.png)

## Visualization dasboard

The dasboard will be found on http://localhost:8050/

![Visualization dashboard](screenshots/dashboard.png)


## pgAdmin

pgAdmin can be accessed on http://localhost:5050 with username `pgadmin@pgadmin.org` and password `admin`


## Database

The postgress DB can be accessed at the following address:
`postgresql://root:root@localhost:5432/sales`

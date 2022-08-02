# Fully dockerized FastAPI example application with async Postgres, SQLAlchemy and Alembic

This is a basic template for a microservice oriented fastapi application with postgres database.
I use this to start projects from.

## Description

An in-depth paragraph about your project and overview of use.

## Getting Started

### Dependencies

* Docker Engine
* Docker Compose

### Installing

Before starting, make sure you have the latest version of Docker installed.

Run the following commands to pull this repo from github
```
git clone https://github.com/reinhud/fastapi_postgres_template
cd POSTGRES_TEST_CONTAINER_PORT/src
```
Create the ```.env``` files or modify the ```.env.example``` files:
```
touch .env
echo POSTGRES_CONTAINER_PORT=5432
echo POSTGRES_TEST_CONTAINER_PORT=6543
```
```
touch prod.env
echo POSTGRES_USER="postgres"
echo POSTGRES_PASSWORD="postgres"
echo POSTGRES_SERVER="postgres_container" 
echo POSTGRES_PORT=5432
echo POSTGRES_DB="postgres"
echo PGADMIN_DEFAULT_EMAIL="pgadmin4@pgadmin.org"
echo PGADMIN_DEFAULT_PASSWORD="postgres"
echo PGADMIN_LISTEN_PORT=80
```

### Run with docker

You must have ```docker``` and ```docker-compose``` tools installed to work with material in this section.
Head to the ```/src``` folder of the project.
To run the program, we spin up the containers with
```
docker-compose up
```
If this is the first time bringing up the project, you need to build the images first:
```
docker-compose up --build
```

### Applying database migrations
In testing, newest revision will be applied automatically before tests.
To run migrations manually before spinning up the docker containers, go to ```/src``` and:
* Create new revision
```
docker-compose run fastapi_server alembic revision --autogenerate -m "The hottest new db changes around"
```
This will try to capture the newest changes automatically.
Check that the changes were correctly mapped by looking into 
the revision file in ```/microservices/fastapi_server/migrations/versions```
* Apply migrations
```
docker-compose run fastapi_server alembic upgrade head
```

### Testing
Make sure you have build the app in ```Docker``` before running tests.
Head to ```/src``` folder and run:
```
docker-compose run fastapi_server pytest .
```


Common issues:

### Web routes
All routes are available on ```/docs``` or ```/redoc``` paths with Swagger or Redoc


## Authors

@Lukas Reinhardt
## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments
Inspiration, code snippets, etc.
* FastAPI Realworl Example - https://github.com/nsidnev/fastapi-realworld-example-app/blob/master/README.rst
* SQLAlchemy async test suite - https://github.com/sqlalchemy/sqlalchemy/issues/5811
* Phresh FastAPI Tutorial Series - https://github.com/Jastor11/phresh-tutorial/tree/master

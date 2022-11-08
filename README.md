# Videoshare

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://gitlab.com/dejan.knezevic/address-book/-/blob/main/LICENSE)


## Requirements

- Python 3.10

## Installation

Clone the repository with:
```bash
git clone git@github.com:QuicksilverMachine/videoshare.git
```

### Backend server configuration

Install development requirements with:
```bash
pip install -r requirements-dev.txt
```

#### Initialize database for testing

By default, database will be a SQLite file for easier local testing, though the models are compatible with PostgreSQL.
To change the database to PostgreSQL, create a database `videoshare` with a role `videoshare` with the password `videoshare`,
and set the environment variable:
```
SQLALCHEMY_DATABASE_URI=postgresql://videoshare:videoshare@localhost:5432/videoshare
```

To generate database run migrations with:
```bash
flask db upgrade
```

Basic database records for local testing can be generated using a custom cli command:
```bash
flask dev init-db
```


### Frontend application configuration

Install requirements (using npm) with:
```bash
npm install
```


## Configuration

### Server

Set app environment variable before starting server:
```
FLASK_APP=videoshare.wsgi
```
### Frontend

Set environment variables for server before starting frontend application:
```
REACT_APP_VIDEOSHARE_SERVER_URL=http://localhost:5000
```

## Running the server

Server can be started for local development using:
```bash
flask run
```
This will start a local server on http://localhost:5000.

## Running the frontend

```bash
npm start
```

Frontend will start the server at http://localhost:3000.


## OpenAPI Schema

The service's OpenAPI schema can be accessed on the server's `/docs` address. 
This auto-documenting page will allow the user to easily test all endpoints.

## Development

A pre-commit hook is available for this project, it can be installed with:
```bash
pre-commit install
```
It will automatically run all backend checks before each commit, but can also be run manually on all files with:
```bash
pre-commit run -a
```

## Additional notes

### Database
For this basic use case SQLite was enough since actual deployment is not planned, and it is simpler to test locally,
even with a single session restriction. Otherwise, PostgreSql would be used with the `psycopg2-binary` package for the
database driver.

### Logging and events
Events could be generated and sent to something like Kafka for later processing.

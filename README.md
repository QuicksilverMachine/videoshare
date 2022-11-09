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

Set app environment variable before using server or cli:
```bash
export FLASK_APP=videoshare.wsgi
```

### Initialize database for testing

By default, database will be a SQLite file for easier local testing, though the models are compatible with PostgreSQL.
To change the database to PostgreSQL, create a database `videoshare` with a role `videoshare` with the password `videoshare`,
and set the environment variable:
```bash
export SQLALCHEMY_DATABASE_URI=postgresql://videoshare:videoshare@localhost:5432/videoshare
```
For this basic use case SQLite was enough since actual deployment is not planned, and it is simpler to test locally,
even with a single session restriction. Otherwise, PostgreSql would be used with the `psycopg2-binary` package for the
database driver.

To generate database run migrations with:
```bash
flask db upgrade
```

Basic database records for local testing can be generated using a custom cli command:
```bash
flask dev init-db
```


### Frontend application configuration

Frontend is located in the same repository as the server, in the `frontend` folder.

Install requirements (using npm) with:
```bash
npm install
```

Set environment variables for server before using the frontend application:
```bash
export REACT_APP_VIDEOSHARE_SERVER_URL=http://localhost:5000
```

## Running the server

Server can be started for local development using:
```bash
flask run
```
This will start a local server on http://localhost:5000.

## Running the frontend

Enter the frontend directory and run:
```bash
npm start
```

Frontend will start the server at http://localhost:3000.


## Usage

The UI contains three main sections: path, control strip and contents.

Next to the path is a button that enables copying the current folder path.

Various controls exist on the control strip:
- Navigation to the parent folder if it exists
- Creation of new videos and folders
- Moving the selected node one folder up

Finally, the contents section is populated by videos and folders that can be moved around by 
dragging and dropping them into other folders, while keeping in mind that node names are unique 
per folder. Clicking on the node will select it, enabling the "move up" function on the control strip.


## OpenAPI Schema

The service's OpenAPI schema can be accessed on the server's root address. 
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

## Tests

Running tests on the server is done with:
```bash
pytest
```
Not everything is currently covered with backend tests, but most of the 
unique situations should be. There can be a lot more tests for special cases for each endpoint.

Running tests on the frontend is done with:
```bash
npm test
```
There is very little testing done on frontend side, as I'm not experienced on that front.

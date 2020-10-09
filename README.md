# Problem Spec

This codebase should serve ReST API endpoints for individual Song management in an iTunes/Spotify-like app.

## Functionality

It should have the following functionality:

- Create a Song
- Delete a Song
- Play a Song
- Update a Song

### Play Stream Stub

All songs have a related file somewhere in the cloud. This file can be accessed via a helper function you should stub.

This function takes a song path (Text) and returns a stream of binary data.

## Database Constraints

A Song should be a row in a database table named `"songs"`

Each Song should have the following properties:

- ID (should be assigned using uuid v4 at song creation)
- Name (character field between 0 and 255 characters)
- Genre (an ENUM with valid values of "Rock", "Pop", "Rap", and "R&B")
- Artist (character field between 0 and 255 characters)
- Length (in seconds)
- Song mp3 file path (text field with max length of 2056 characters)
- Ranking (an unsigned integer with valid values from 0 to 5)

## Deliverable

**1. Source Code**: Written in Python using Flask framework, with Postgres Database. Third-party libraries included in `/backend/requirements.txt`

**2. Tests**: Written side-by-side to relevant code to increase exportability of code (ex. `/backend/project/app.py` has test file `/backend/project/app_test.py`)

**3. Documentation**: Written in this README and in Python comments

# Documentation

## Source Code Overview

- Root Directory contains environment variables for Docker-Compose to consume and use when building / launching containers
- Backend Directory contains Dockerfile, a shell script `entrypoint.sh` that tells the backend to wait for Postgres to be available before starting, `requirements.txt` for third party python libraries needed, and `manage.py` script to run one-off commands. It also has the following directories:
  - config: settings for Gunicorn server and Flask App (sourced from `.env` file for secrecy / portability)
  - lib: utility functions for use in this project
  - cli_commands: python scripts containing instructions that can be used after calling `python manage.py` (ex. `test`, and `db reset`)
  - atticus_tunes: main Flask app directory
    - `db.py`: Connection to Postgres database connected to instance of Flask
    - `extensions.py`: Contains instance of database connection class to initialize with an instance of Flask
    - `app.py`: Provides Flask App instance via `create_app()` factory pattern
    - `song/`: Contains files and tests related to Song API
      - `interface.py`: Type Hint for dictionaries involved with making Song objects
      - `model.py`: Python Object representation of a Song
      - `schema.py`: Bridge layer between external data and Python Model of Song
      - `service.py`: Performs database operations pertaining to Songs
      - `routes.py`: Provides endpoints for Flask App to be consumed by user (using Flask Blueprint pattern)

## API

Base url defaults to `localhost:5000`

**NOTE** Examples Executed in order starting with POST

- `/health` --> Accepts GET, Responds with JSON data with 200 status code if working

example:

```bash
curl -X GET http://localhost:5000/health
```

- `/songs/` --> Accepts POST with JSON body, Responds with JSON data. Success Response if JSON body is saved as a Song entry in database, else Error Response.

example:

```bash
curl -d '{"name": "songname", "ranking": 2, "genre": "Rap", "artist": "me
", "length": 5, "song": "/place/file.mp3"}' -H 'Content-Type: application/json' -X POST http://localhost:5000/songs/

# Returns
{
  "artist": "me",
  "genre": "Rap",
  "id": "09d929f6-87a8-42e0-9928-6eb4761bc93b",
  "length": 5,
  "name": "songname",
  "ranking": 2,
  "song": "/place/file.mp3"
}
```

- `/songs/{id}` --> Accepts GET with a valid UUID in place of `{id}`, Responds with Streamed Binary Data or JSON data. Success Stream response if the id exists in database and cloud service can find the song file path, else Error JSON Response

example:

```bash
curl -X GET http://localhost:5000/songs/09d929f6-87a8-42e0-9928-6eb4761bc93b

# Returns
Fake Data Stub
```

- `/songs/{id}` --> Accepts PUT with a valid UUID in place of `{id}` and JSON body, Responds with JSON data. Success Response if JSON body is valid and updates the song with given ID in database, else Error Response.

example:

```bash
curl -d '{"name": "other song name", "artist": "another person"}' -H 'Content-Type: application/json' -X PUT http://localhost:5000/songs/09d929f6-87a8-42e0-9928-6eb4761bc93b

# Returns
{
  "artist": "another person",
  "genre": "Rap",
  "id": "09d929f6-87a8-42e0-9928-6eb4761bc93b",
  "length": 5,
  "name": "other song name",
  "ranking": 2,
  "song": "/place/file.mp3"
}
```

- `/songs/{id}` --> Accepts DELETE with a valid UUID in place of `{id}`, Responds with JSON data. Success Response if Song with given ID is deleted from database, else Error Response.

example:

```bash
curl -X DELETE http://localhost:5000/songs/09d929f6-87a8-42e0-9928-6eb4761bc93b

# Returns
{
  "message": "Success"
}
```

## Third Party Libraries Used

- Flask, web framework for Python, used for handling requests and responses
- Gunicorn, python wsgi web server for running Flask app
- Psycopg2, python binding for Postgres DBAPI. Not an ORM like SQLAlchemy.
- Marshmallow & Webargs, Data Serialization / De-Serialization library for validating request json data and dumping Python objects to json data
- Pytest & Coverage, Testing library for running tests with re-usable fixtures

# Install and Run

Deployed using `docker-compose`

- Download or clone repository and `cd` into it

```bash
git clone git@github.com:gerardrbentley/atticus-tunes.git tunes
cd tunes
```

- Run Tests to confirm it's functional

```bash
# --rm removes container after use, see /backend/cli_commands/test_cmd.py for more
docker-compose build
docker-compose run --rm backend python manage.py test
```

- Run docker-compose up to launch

```bash
# Use `-d` flag to ignore logs and free up your terminal window
docker-compose up --build
# Spins up containers for flask backend with hot-reload, postgres instance,
# available at localhost:5000 (or docker-machine / virtual machine IP)
# Automatically resets and seeds database per /backend/entrypoint.sh
```

- Visit or curl http://localhost:5000/health

- Use `ctrl+c` to shut down (or `docker-compose down` if using `-d` flag for up call)

# Docker Notes

- Use `docker-compose down --volumes` to erase / free up postgres data

# Resources

- [Flask Python Framework](https://flask.palletsprojects.com/en/1.1.x/)
- [API Pattern](http://alanpryorjr.com/2019-05-20-flask-api-example/)

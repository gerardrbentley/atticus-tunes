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

Deployed using `docker-compose`

# Install and Run

- Download or clone repository and `cd` into it

```bash
git clone # TODO: link backend
cd backend
```

- Run Tests to confirm it's functional

```bash
# --rm removes container after use, see /backend/cli_commands/test_cmd.py for more
docker-compose run --rm backend python manage.py test

# or test production setup (not volume mounted)
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml run --rm backend python manage.py test
```

- Run docker-compose up to launch

```bash
# Use `-d` flag to ignore logs and free up your terminal window
docker-compose up --build
# Spins up containers for flask backend with hot-reload, postgres instance,
# available at localhost:5000 (or docker-machine / virtual machine IP)
# Automatically resets and seeds database per /backend/entrypoint.sh

# or run production build
docker-compose -f docker-compose.prod.yml up --build
# Requires Initializing database via one-off backend container or with running container
# (in a new terminal tab/window if not using `-detach` up flag)
# (See https://docs.docker.com/compose/reference/run/ for more info)

# Runs `python manage.py db reset` to initialize and seed postgres db
# (See /backend/cli_commands/db_cmd.py)
docker-compose run --rm backend python manage.py db reset --with-test
```

- Visit or curl http://localhost:5000/health

- Use `ctrl+c` to shut down (or `docker-compose down` if using `-d` flag for up call)

# Docker Notes

- Use `docker-compose down` or `docker-compose -f docker-compose.prod.yml down` before switching to the other deployment. ('db' service needs to drop the database volume it's currently attached to)
- Use `docker-compose down --volumes` to erase / free up postgres data

# Resources

- [Flask Python Framework](https://flask.palletsprojects.com/en/1.1.x/)
- [API Pattern](http://alanpryorjr.com/2019-05-20-flask-api-example/)

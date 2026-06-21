# Acampabàsquet

This app will manage a 24 hours basketball championship

## Installation

Make sure you have installed in your OS
```
docker
```

Then run:
```
docker-compose up --build
```

## Docker commands
- Run tests: `docker-compose run web python manage.py test tests`
- Run management commands: `docker-compose run web python manage.py <command>`

## Run tests
Run `make tests`. It will do isort-check, lint and django tests.

## Utils
- Update packages: `make requirements`. Creates a requirements.txt file with the last versions of the packages inside requirements/base.txt. You can run it whenever you want to update your project. It will create a temporary virtualenv.
- `make virtualenv` Creates a new virtualenv using requirements.txt.
- `make virtualenv_test` Creates a development virtualenv using requirements.txt and packages from requirements/test.txt.
- `make clean` Removes the .pyc files and deletes the virtualenv folder.
- `make isort` Checks your code and fixes the imports using isort.
- `make run` Will execute a runserver with development settings.
- `make makemigrations` Will execute a makemigrations with development settings.
- `make migrate` Will execute a migrate with development settings.

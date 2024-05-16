# Django project for Gabriel Iovu
Includes all the basic functionality for django project + djangoui

## Table of content

---
- [Requirements](#requirements)
- [Installation](#installation)

---

## Requirements
1. [Docker](https://www.docker.com/products/docker-desktop/)
2. [Python](https://www.python.org/downloads/)
3. Virtual environment of choice (virtualenv, venv, virtualenvwrapper...)
4. [Pytest](https://docs.pytest.org/en/7.1.x/)


## Installation
1. Create a virtual environment matching the Python version `python3.10 -m venv venv`
2. Start the virtual environment: `source venv/bin/activate`
3. Run `make requirements`
4. Create env directory `mkdir .env && cp .env.example .env/.dev-sample`
5. Source the env file by running `source .env/.dev-sample`
6. Run `docker compose build`
7. Run `docker compose up` starts the docker or `docker compose up -d` starts the docker without
the logs.


#### [optional steps if you do not use docker]
8. Run `python manage.py collectstatic --no-input`
9. Run `make migrate` runs the migrations or `python manage.py migrate`.
10. Create a superuser by running `python manage.py createsuperuser` and use the email added to `.env`.
11. Run `make run` starts the development server or `python manage.py runserver 0.0.0.0:8001 --insecure`.

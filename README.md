## Django URL Shortener

A Django application for creating a shortened URL.

For example, you have a URL like this: https://www.example.com/a-really-long-path-here

This app will shorten it to something like: http://127.0.0.1/G7dt9mY (of course the protocol and domain may differ in your scenario).

Redis caching is utilized for the short path and the timeout can be adjusted in .env.

ClickHouse and RabbitMQ are being used to implement click tracking, this is WIP.

### Installation

These steps will guide you through setting up this app using the minimum requirements (sqlite3 database, hosted at localhost).

It is recommended to install the requirements into and run python from a virtual env. Adjust the name of your pip/python binaries or paths as needed.

#### 1. Clone this repo

Clone this repo into a directory where you would like to store the source files.

`git clone giturl .`

Replace "giturl" with the actual git URL of this repo.

#### 2. Launch the Redis, ClickHouse, and RabbitMQ Docker container

This step assumes you have Docker and Docker Compose installed.

Navigate into the `docker` folder in this repo and run:

`docker-compose up -d`

Use the `docker ps` command to check if the containers launched and are running without crashing.

#### 3. Install requirements

Navigate to the directory where you cloned the source. You should be at the same level as requirements.txt and manage.py. Use the following command to install any required python packages:

`pip install -r requirements.txt`

#### 4. Environment variables

Copy .env.sample to .env and open the file. Make changes as necessary to configure database details, allowed hosts, debug mode, etc. 

To generate a secret key, run these commands from inside a python3 shell:

```
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```

#### 5. Database migrations

Use the following command to set up the database:

`python manage.py migrate`

#### 6. Create a superuser

Use the following command to create a superuser:

`python manage.py createsuperuser`

#### 7. Run tests

Use the following command to run tests:

`python manage.py test`

The tests should all pass. Please file an issue if they don't.

#### 8. Run application

Use the following command to run the application on localhost:

`python manage.py runserver`

You should then be able to access http://127.0.0.1:8000/ in a browser and see form for creating a shortened URL. Please file an issue if you are unable to after performing all of the above steps.

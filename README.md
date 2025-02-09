## Django URL Shortener

A Django application for creating a shortened URL.

For example, you have a URL like this: https://www.example.com/a-really-long-path-here

This app will shorten it to something like: http://127.0.0.1/G7dt9mY (of course the protocol and domain may differ in your scenario).

Redis caching is utilized for the shortened URL and the timeout can be adjusted in .env.

ClickHouse and Celery/RabbitMQ are used to implement click tracking.

### Installation

These steps will guide you through setting up this app using the minimum requirements.

#### 1. Clone this repo

Clone this repo into a directory where you would like to store the source files.

`git clone giturl`

Replace "giturl" with the actual git URL of this repo.

#### 2. Copy .env.sample to .env and configure

Navigate into the project directory:

`cd django-url-shortener`

Copy .env.sample to .env:

`cp .env.sample .env`

Open .env in your favorite text editor and configure the variables. At the very minimum, you will need to set a DJANGO_SECRET_KEY. You may use the secret key generator script in this project:

`python3 secret_key_generator.py`

The remaining variables are set for local testing and development but any passwords and usernames would need to be changed for production environments.

#### 3. Launch the Docker containers

This step assumes you have Docker and Docker Compose installed.

Run the following to build and launch the containers:

```
docker-compose build
docker-compose up -d
```

Use the `docker ps` command to check if the containers launched and are running without crashing.

#### 4. Create a Django superuser

Run the following to create a Django superuser:

`docker exec -it django-app python manage.py createsuperuser`

#### 5. Run tests

TODO

#### 6. Run application

At this point you should then be able to access http://127.0.0.1/ in a browser and see form for creating a shortened URL.

The admin area is located at http://127.0.0.1/admin .

#### 7. Create some captcha questions and answers

Log into the admin area and navigate to "Captchas" under "Main" on the left. Create several question and answers.

### API Documentation

TODO

### Roadmap

- Allow anonymous users to create API keys (restrict by IP? require email verification?)
- Add API request rate limiting
- Automatically load some starting captcha question and answers into the database
- Document running tests with the new Docker setup
- Automatically create a superuser based on .env variables
- Document API

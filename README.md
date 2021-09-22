# Hedera

Hedera is an application for viewing texts in different languages such that:
- pedagogical aids such as glosses can assist the reader;
- the reader can track personal vocabulary lists;
- the reader can refer to shared vocabulary lists;
- texts can be organized into classes;
- and a reader can see how much of a text should already be familiar.

## Getting Started

### With Docker (compose)

Before running for the first time (or any time for that matter):

```
docker-compose build
```

To run the app:

```
docker-compose up
```

When are you are finished, simply hit `ctrl-c` and the containers will shutdown.

On initial running, you might want do run the following in another terminal:

```
docker-compose run django python manage.py create_cms
```

To import lattice data:

```
docker-compose run django python manage.py shell -c "import load_ivy_lattice"
docker-compose run django python manage.py shell -c "import logeion_load"
```

(Optional) Chinese lattice data:

**Caution**: _This can take more than one hour._

```sh
docker-compose run django python manage.py shell -c "import load_chinese_lattice"
```

#### Good to know's and Gotcha's

Steps to add a new python package:

1. Add package to `Pipfile`
2. Run `docker-compose run django pipenv lock`. This will save/update the `Pipfile.lock` file.
3. Note that the django container must be running before executing the next command.
4. Run:
    ```
    docker-compose exec django pipenv install --system
    docker-compose exec worker pipenv install --system
    ```

If you'd like to remove all existing images and start fresh:

```
docker-compose down --rmi all
docker-compose build
docker-compose up
```

If you've run a lot of containers and you'd like to clean them up so that your `docker compose` command output isn't endless:

```
docker ps --filter status=exited --filter name=hedera_django_run -q | xargs docker rm
```

### Without Docker

You'll need Redis running.  To get it going locally on the Mac, simply run:

```
brew install redis
```

and either
`brew services start redis` to always start redis
or `redis-server /usr/local/etc/redis.conf` to run it one time.


```
npm install
pipenv install
pipenv shell
createdb hedera
./manage.py migrate
./manage.py loaddata sites
./manage.py create_cms
```

To import lattice data:

```
./manage.py shell -c "import load_ivy_wonky_words"
./manage.py shell -c "import load_ivy_lattice"
./manage.py shell -c "import logeion_load"
# optional (this can take more than an hour)
# ./manage.py shell -c "import load_chinese_lattice"
```

And finally, to start Django,

```
./manage.py runserver
```

By default, there is a background worker that will work synchronously (won't need the worker running to process the lemmatization).  If you want to process asynchronously locally:

```
export RQ_ASYNC=1
./manage.py runserver
```

Then in another terminal:

```
pipenv shell
export RQ_ASYNC=1
./manage.py rqworker ${RQ_QUEUES:-default}
```

Leave the first two Terminal windows running. Open a third Terminal window and run:

```
npm start
```

Browse to http://localhost:8000/


You many want to sign up and activate an account on a local desktop/laptop. After signing up, you will see an error stating that the is not active. Since you probably won't be receiving an email, the easiest way to activate it is to run the following commands:

```
cd <path to hedera repo>
pipenv shell
./manage.py shell
```

In the shell, type:

```
from django.contrib.auth.models import User
user = User.objects.get(pk=1)
user.is_active = True
user.save()
```


## PDF Service

To enable the PDF export of a learner's text with gloss you need to run the PDF
service that is packaged up as a docker container.

For local development:

```
docker run --publish 9000:9000 --env X_API_KEY=test-secret eldarioninc/pdf-service
```

## Contributing Guidelines

### Linting

This project uses `isort` for import sorting, `flake8` for Python linting, and various `eslint plugins` for Javascript linting.

### Passing Builds via Github

#### Pre-commit

To make developement more streamlined we have implemented a pre-commit package manager to manage pre-commit hooks for python and javascript
- Install [Pre-commit](https://pre-commit.com/)
Note: the installation guide covers different install methods
- you will then need to run the following command in the root of the project
```
pre-commit install
```
You're all set! Now when you commit code upstream the commit will trigger the different linters and flag the required changes
Notes: you can quickly fix javascript eslint errors with `npm run lint:fix`

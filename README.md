# Hedera

This is a minimalistic project that just has basic account features and a simple, static reader [or will—this is a work in progress].

For the full Scaife Viewer running the Perseus Digital Library in production, see <https://github.com/scaife-viewer/scaife-viewer>.

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

#### Good to know's and Gotcha's

Steps to add a new python package:

1. Add package to `Pipfile`
2. Run `docker-compose run django pipenv lock`. This will save/update the `Pipfile.lock` file.
3. Note that the django container must be running before executing the next command. 
4. Run `docker-compose exec django pipenv install --system`.

If you'd like to remove all existing images and start fresh:

```
docker-compose down --rmi all
docker-compose build
docker-compose up
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


## Resetting the Database

Every so often, it may be requested that the dev DB be "reset." Meaning, tables from the lattices, lemmatized_text, and vocab_list be truncated, and the data for lattices will be reloaded. User account information should be preserved. You can do that with the following set of commands. Note that these commands are for executing against a running docker container. If you are running the project in another way, adjust the incantations accordingly.

```sh
# Run the custom management command to delete all of the relevant data.
# The --no_input flag answers 'yes' to all prompts asking if you'd like to delete data.
# Run without --no_input if you'd like to step through the process interatctively.
$ docker-compose exec django python manage.py reset_db --no_input

# Run commands to reload the data
$ docker-compose exec django python manage.py shell -c "import load_ivy_wonky_words"
$ docker-compose exec django python manage.py shell -c "import load_ivy_lattice"
$ docker-compose exec django python manage.py shell -c "import logeion_load"
$ docker-compose exec django python manage.py shell -c "import load_clancy_lattice"
```

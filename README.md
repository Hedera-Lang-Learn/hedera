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

```sh
# first, build the prod django image
docker compose build npm
# next, build the dev images
docker compose build
```

* **Details:** Local development uses two images, one built with the `Dockerfile` (this is the production image), and a derivative image built with the `Dockerfile.dev` (this is the development image; it simply adds dev dependencies as an extra layer to the prod image). The `npm` docker compose service uses the production image, and the `django` and `worker` services use the development image.

To run the app:

```
docker compose up
```

When are you are finished, simply hit `ctrl-c` and the containers will shutdown.

On initial running, you might want do run the following in another terminal:

```
docker compose run --rm django python manage.py create_cms
```

To import lattice data:

```
docker compose run --rm django python manage.py shell -c "import load_ivy_lattice"
docker compose run --rm django python manage.py shell -c "import logeion_load"
```

(Optional) Chinese lattice data:

**Caution**: _This can take more than one hour._

```sh
docker compose run --rm django python manage.py shell -c "import load_chinese_lattice"
```

#### **Good to know's and Gotcha's**

Steps to add a new python package:
Prequisite - Install pip-compile into your virtual env via this command `python -m pip install pip-tools`. [Documentation here](https://github.com/jazzband/pip-tools)
1. Add package to `hedera/requirements/base.in`
2. Note that the django container must be running before executing the next command.
3. Run:
    ```
    pip-compile hedera/requirements/base.in --output-file=- > hedera/requirements/base.txt
    docker compose exec django pip install <package>
    docker compose exec worker pip install <package>
    ```
    Note: Alternatively we could also rebuild the images for npm, django and worker after running `pip-compile hedera/requirements/base.in --output-file=- > hedera/requirements/base.txt` via these commands:
    ```sh
    # rebuild the base/prod image
    docker compose build npm
    # rebuild the dev images
    docker compose build django
    docker compose build worker
    ```
Note/TODO: We will have to update how we run the exec commands with root in favor of a designated user. Running the above exec commands will cause the following warning flag:
```diff
- Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager.
```

If you'd like to remove all existing images and start fresh:

```sh
docker compose down --rmi all
# first, build the prod django image
docker compose build npm
# next, build the dev images
docker compose build
docker compose up
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

1. Install node dependencies run `npm install`
2. use pyenv virtualenv to create a virtual environment with python 3.7 or higher ([pyenv virtual install instructions here](https://github.com/pyenv/pyenv-virtualenv#installing-with-homebrew-for-macos-users)). Activate the virtual environment and run the following commands:
```
pip install -r hedera/requirements/base.txt
createdb hedera
./manage.py migrate
./manage.py loaddata sites
./manage.py create_cms
```
3. To import lattice data:

```
./manage.py shell -c "import load_ivy_wonky_words"
./manage.py shell -c "import load_ivy_lattice"
./manage.py shell -c "import logeion_load"
# optional (this can take more than an hour)
# ./manage.py shell -c "import load_chinese_lattice"
```
4. And finally, to start Django,

```
./manage.py runserver
```

By default, there is a background worker that will work synchronously (won't need the worker running to process the lemmatization).  If you want to process asynchronously locally:

```
export RQ_ASYNC=1
./manage.py runserver
```

Then in another terminal(activate the virtual environment via pyenv):

```
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

To make developement more streamlined we have implemented a pre-commit package manager to manage pre-commit hooks for python and javascript.
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
$ docker compose exec django python manage.py reset_db --no_input

# Run commands to reload the data
$ docker compose exec django python manage.py shell -c "import load_ivy_wonky_words"
$ docker compose exec django python manage.py shell -c "import load_ivy_lattice"
$ docker compose exec django python manage.py shell -c "import logeion_load"
$ docker compose exec django python manage.py shell -c "import load_clancy_lattice"
$ docker compose exec django python manage.py shell -c "import load_chinese_lattice"
```

## Adding a new language

In order to add a new language, you will need to add an entry to `SUPPORTED_LANGUAGES` in `hedera.supported_languages.py`. Every language requires a "code", "verbose_name", "service", and "tokenizer." Language specific services are defined in `lemmatization.services`. Please, review the existing services and tokenizers, and add your language's module.

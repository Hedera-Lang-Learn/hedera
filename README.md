# Hedera

Hedera is an application for viewing texts in different languages such that:
- pedagogical aids such as glosses can assist the reader;
- the reader can track personal vocabulary lists;
- the reader can refer to shared vocabulary lists;
- texts can be organized into classes;
- and a reader can see how much of a text should already be familiar.

## Getting Started

### With Docker Compose
You will need to have docker installed, use the following link to [install docker](https://docs.docker.com/get-docker/) into your respective OS

To run the app:

```
docker compose up
```

When are you are finished, simply hit `ctrl-c` and the containers will shutdown.

On initial running, you might want do run the following in another terminal:

```
docker compose run --rm django python manage.py create_cms
```
#### Importing Data
To import data into the database:

```
docker compose run --rm django python manage.py shell -c "import loaders.lat.load_latin_lemma"
docker compose run --rm django python manage.py shell -c "import loaders.lat.load_latin_form_to_lemma"
docker compose run --rm django python manage.py shell -c "import loaders.lat.load_latin_gloss"
docker compose run --rm django python manage.py shell -c "import loaders.lat.load_latin_vocab"
```

<!-- TODO UPDATE -->
(Optional) Chinese lattice data:

**Caution**: _This can take more than one hour._

```sh
docker compose run --rm django python manage.py shell -c "import loaders.zho.load_chinese_lattice"
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
    Note: Alternatively we could also rebuild the images for the `django` and `worker` services after running `pip-compile hedera/requirements/base.in --output-file=- > hedera/requirements/base.txt` via these commands:
    ```sh
    docker compose build django
    docker compose build worker
    ```

If you'd like to remove all existing images and start fresh:

```sh
docker compose down --rmi all
docker compose build
docker compose up
```

Note: This will not remove the data in the database, to keep from having to re-load the language data. If you want to remove the database, you can remove `./.docker-data` in this directory. This is specified in the `docker-compose.yml`, s if that doesn't work you can check if the configuration has changed there.

If you've run a lot of containers and you'd like to clean them up so that your `docker compose` command output isn't endless:

```
docker ps --filter status=exited --filter name=hedera_django_run -q | xargs docker rm
```

##### Font Awesome Kit
Notes: base.html is using a js file provided by Font Awesome Kit `https://kit.fontawesome.com/2db98e34e3.js`. This means that icons like the familarity and edit buttons will stop working if the link expires. Link is created from [Font Awesome Kit Setup](https://fontawesome.com/docs/web/setup/use-kit). We could download the js file and run it locally as well, but will hold off for now.

## PDF Service

To enable the PDF export of a learner's text with gloss you need to run the PDF
service that is packaged up as a docker container.

For local development:

```
docker run --publish 9000:9000 --env X_API_KEY=test-secret eldarioninc/pdf-service
```

## Contributing Guidelines

### Tests

#### Frontend / Javascript

There are some tests for the Vue frontend code:

```
npm run test:unit
```

#### Backend / Python

Unit tests depend on:
* a connection to a postgres DB; this is due to limitations in the `django-lti-provider` package; see `test_settings.py`), and
* a connection to redis (`django-rq` requires a redis connection, with no simply way to mock it for tests).

Here's one way to run them, using the containerized app, which is already configured to look for the required support services on the docker container network:

```
docker compose up -d postgres redis
# make sure postgres and redis are available, then run:
docker compose run --rm --no-deps --service-ports -e DJANGO_SETTINGS_MODULE=hedera.test_settings django python manage.py test
```

You can also run them locally (i.e. not in a container) if you have the appropriate python environment configured. For instance:

```
docker compose up -d postgres redis
# make sure postgres and redis are available, then run:
DJANGO_SETTINGS_MODULE=hedera.test_settings python manage.py test
```
##### Note:
    To log out entire diff in a test set self.maxDiff = None
    https://docs.python.org/3/library/unittest.html#unittest.TestCase.maxDiff

### Linting

This project uses `isort` for import sorting, `flake8` for Python linting, and various `eslint plugins` for Javascript linting.

### Passing Builds via Github

The GitHub Actions workflow .github/workflows/ci.yaml runs the unit tests and various code quality checks.

#### Pre-commit

To make development more streamlined we have implemented a pre-commit package manager to manage pre-commit hooks for python and javascript.
- Install [Pre-commit](https://pre-commit.com/)
Note: the installation guide covers different install methods
- you will then need to run the following command in the root of the project
```
pre-commit install
```
You're all set! Now when you commit code upstream the commit will trigger the different linters and flag the required changes
Notes: you can quickly fix javascript eslint errors with `npm run lint:fix`


## Resetting the Database

Every so often, it may be requested that the dev DB be "reset." Meaning, tables from the lemma, lemmatized_text, and vocab_list be truncated, and the data for lemmas will be reloaded. User account information should be preserved. You can do that with the following set of commands. Note that these commands are for executing against a running docker container. If you are running the project in another way, adjust the incantations accordingly.

```sh
# Run the custom management command to delete all of the relevant data.
# The --no_input flag answers 'yes' to all prompts asking if you'd like to delete data.
# Run without --no_input if you'd like to step through the process interatctively.
$ docker compose exec django python manage.py reset_db --no_input
```
Run commands from the [importing data step](#importing-data) to reload the data

## Adding a new language

In order to add a new language, you will need to add an entry to `SUPPORTED_LANGUAGES` in `hedera.supported_languages.py`. Every language requires a "code", "verbose_name", "service", and "tokenizer." Language specific services are defined in `lemmatization.services`. Please, review the existing services and tokenizers, and add your language's module.

## Debugging Programmatically

To debug from within vscode you can enter this line into the file/endpoint you want to debug. [Reference to debugger](https://code.visualstudio.com/docs/editor/debugging) and [debugpy vscode reference](https://code.visualstudio.com/docs/python/debugging)
```python
        import debugpy

        try:
            debugpy.listen(("0.0.0.0", 5678))
            print("Waiting for debugger attach")
            debugpy.wait_for_client()
            debugpy.breakpoint()
            print('break on this line')
        except:
            pass

```
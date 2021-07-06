# Hedera

This is a minimalistic project that just has basic account features and a simple, static reader [or will—this is a work in progress].

For the full Scaife Viewer running the Perseus Digital Library in production, see <https://github.com/scaife-viewer/scaife-viewer>.

## Getting Started

### With Docker

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
##### Python Linting
- Install `isort` and `flake8` into either your local virtual environment terminal or directly into the Docker `hedera-postgres` container terminal
    
    ```bash
    pip install isort flake8
    ```
    After installing you can now run the the `isort` command in the terminal to check import sorting
    ```bash
    isort -c **/*.py
    ```
    and then run the following `flake8` command to lint python
    ```bash
    flake8 --show-source databasetext hedera lattices lemmatization lemmatized_text vocab_list lti
    ```

##### Javascript Linting
- The linting packages should be installed from the setup instructions as noted above. We can run the following command in either your local terminal or in the docker `hedera-npm
` container terminal
    ```bash
    npm run lint
    ```

# Hedera

This is a minimalistic project that just has basic account features and a simple, static reader [or will—this is a work in progress].

For the full Scaife Viewer running the Perseus Digital Library in production, see <https://github.com/scaife-viewer/scaife-viewer>.

## Getting Started

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
```

To import vocabulary list data (whichever ones you want):

```
./manage.py shell -c "import dcc_latin_morpheus_load"
./manage.py shell -c "import shelmerdine_load"
./manage.py shell -c "import logeion_load"
```

Note: the last one takes a long time (potentially longer than an hour) and is mostly useful just to get a lot of glosses for words not in the DCC (or other) vocabulary lists.

And finally, to start Django,

```
./manage.py runserver
```

By default, the there is a background worker that will work synchronously (won't need the worker running to process the lemmatization).  If you want to process asynchronously locally:

```
export RQ_ASYNC=1
./manage.py runserver
```

Then in another terminal:

```
export RQ_ASYNC=1
./manage.py rqworker ${RQ_QUEUES:-default}
```

Leave the first two Terminal windows running. Open a third Terminal window and run:

```
cd <path to hedera repo>
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

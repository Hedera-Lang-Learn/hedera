# Hedera

This is a minimalistic project that just has basic account features and a simple, static reader [or will—this is a work in progress].

For the full Scaife Viewer running the Perseus Digital Library in production, see <https://github.com/scaife-viewer/scaife-viewer>.

## Getting Started

```
npm install
pipenv run pip install pip==18.0
pipenv install
pipenv shell
createdb hedera
./manage.py migrate
./manage.py loaddata sites lattices cana livy tolstoy gnt80 morphgnt-lemmatization dcc_latin
./manage.py runserver
```

Leave the first Terminal window (above) running. Open a second Terminal window and run:

```
cd <path to hedera repo>
npm start
```

Browse to http://localhost:8000/ or http://localhost:8000/read/1/


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

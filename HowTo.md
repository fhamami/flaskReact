## VIRTUALENV

$ virtualenv -p python3 venv

##

All configuration file at folder `instance`

`flask.cfg` is main of configurations

to grab the folder of the top-level directory of this project we use

```
BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)
```

SECRET_KEY is came from

```
>>> import os
>>> os.urandom(24)
```

## DATABASE

CREATE USER flaskreact WITH PASSWORD 'password';
CREATE DATABASE flaskreact_db OWNER flaskreact;

## USERS

## POST

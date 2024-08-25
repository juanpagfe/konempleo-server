# Setting up local environment

## Settin up virtual environment

python3 -m venv venv

## Setting up global interpreter

In the palette select Python: Select interpreter and type ./venv/bin/python or ./venv/Scripts/python

## Setting source from virtual environment mac

source venv/bin/activate

### Instaling fast api with dependencies

pip3 install 'fastapi[all]'

### Check python dependencies

pip3 freeze

## Creating/updating requirements.txt lib file

pip3 freeze > requirements.txt

### Run live server

In the root directory
uvicorn app.main:app --reload

### Install dependencies in requirements.txt

pip install -r requirements.txt

## Migrations

### Run migrations

alembic upgrade head

### Generate migration

alembic revision -m 'migration-name'

### Migrations history

alembic history

### Downgrade migration

alembic downgrade -'number of migrations'

### Runinng in server

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app


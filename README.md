# Milk Data

## Prerequisite

    virtualenv venv --python=3.11

    source venv/bin/activate
    
    pip install -r requirements.txt

## Envronment Variable

Create .env variable next to README.md and add thse variables

    DEBUG=1

    <!-- Remaining all are optional -->
    SECRET_KEY=somefakesecretkey
    ALLOWED_HOSTS=localhost
    DATABASE_URL=sqlite:///db.sqlite3


## Development

    python manage.py migrate
    python mangae.py runserver
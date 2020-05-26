# MarXXIsts

Python rewrite of [MarXXIsts](https://github.com/prolesoft/MarXXIsts)

## Building

### Without Docker

To build this project:

1. Ensure that PostgreSQL is installed on your local machine and that its binaries are in your path
1. Ensure that Pandoc is installed on your local machine
1. Create a PostgreSQL database for the application
1. Create a config.cfg file with a line following this template: `SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost:5432/db_name"`
1. Add a line to your config.cfg file following this template: `SECRET_KEY = "key-or-phrase-of-your-choice"`
1. `pip install -r requirements.txt`
1. `flask db upgrade`
1. `flask run`
1. Check out <http://localhost:5000> in your browser.

### With Docker

1. `docker-compose up --build`
1. Check out <http://localhost:5000> in your browser.
# MarXXIsts

MarXXIsts is an online platform for 21st century Marxist thinkers and activists to publish, study, analyse and critique each 
other's theoretical works. In other words, a slightly more robust [marxists.org](https://www.marxists.org) for the work of
Marxists who are still alive and are actively engaging with criticism and analysis of their own work.

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
1. Check out <http://localhost:5000> in your browser

### With Docker

1. `make run` to run
1. Check out <http://localhost:5000> in your browser
1. `make stop` to stop
1. `make build` to build an image

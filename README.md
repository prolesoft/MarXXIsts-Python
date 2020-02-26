# MarXXIsts

Python rewrite of [MarXXIsts](https://github.com/prolesoft/MarXXIsts)

## Building

To build this project:

1. Ensure that PostgreSQL is installed on your local machine
2. Create a PostgreSQL database for the application
3. Create a config.cfg file with a line following this template: `SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost:5432/db_name"`
4. Add a line to your config.cfg file following this template: `SECRET_KEY = "key-or-phrase-of-your-choice"`

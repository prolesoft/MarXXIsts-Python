from flask import Flask, escape, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models

@app.route('/')
def index():
    return render_template('index.html')
# flask-basics

Creating the foundation of a social media app with features like users, user posts, a public feed, and account registration.
Flask Jinja HTML WTForms 


To start, in terminal with the commands:

>>> export FLASK_APP=main.py
>>> export FLASK_DEBUG=1
>>> flask run


To access the database (db):

>>> python3
>>> from main import db, User, UserPost
#Options to drop, or create db
>>> db.drop_all() / db.create_all()


Other commands:

User.query.all()
User.query.filter_by(username='some_string')


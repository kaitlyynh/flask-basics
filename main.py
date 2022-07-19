from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
import datetime

from forms import RegistrationForm, MakePost, SignIn

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SECRET_KEY'] = 'flasksite'
app.config['SQLALCHEMY_BINDS'] = {
    'post_db':'sqlite:///post_db.db'
}

db = SQLAlchemy(app)
post_db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('UserPost', backref='user')

    def __repr__(self):
        return self.username

class UserPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return self.text

#class UserPost(db.Model):
#    __bind_key__ = 'post_db'
#    id = db.Column(db.Integer, primary_key=True)
#    text = db.Column(db.String(250), nullable=False, unique=False)
#
#    def __repr__(self):
#        return self.text

current_date = datetime.datetime.now().strftime("Today is %A, the %-d of %B %Y")
current_date_raw = datetime.datetime.now().strftime("%B-%-d-%Y")
current_time = datetime.datetime.now().strftime("%-I:%M %p")

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    make_post = MakePost()
    if make_post.validate_on_submit():
        post_to_add = UserPost(text=make_post.body.data)
        db.session.add(post_to_add)
        db.session.commit()            
    feed = UserPost.query.all()
    if make_post.errors != {}:
        for message in make_post.errors:
            print(message)
    return render_template('homepage.html', 
        current_date=current_date, 
        current_time=current_time, 
        make_post=make_post,
        feed=feed,
        current_date_raw=current_date_raw
        )

@app.route('/messages')
def message_page():
    return render_template('messages_page.html', current_date=current_date, current_time=current_time)

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in_page():
    sign_in_form = SignIn()
    if sign_in_form.validate_on_submit():
        print("Validated")
        user_to_check = User.query.filter_by(username=sign_in_form.sign_user.data).first()
        if user_to_check == None: #user doesnt exist
            flash('This user does not exist, please see the register page or try again.')
            return redirect(url_for('sign_in_page'))
        else: #user does exist
            return redirect(url_for('home_page'))
    else:
        print("Not validated")
    for errors in sign_in_form.errors:
        print(errors)
    return render_template('sign_in_page.html', current_date=current_date, current_time=current_time, sign_in_form=sign_in_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    info = RegistrationForm()
    if info.validate_on_submit():
        user_to_add = User(username=info.username.data, password=info.password1.data, email=info.email_address.data)
        db.session.add(user_to_add)
        db.session.commit()
        flash("Successfully registered.")
        return redirect(url_for('home_page'))
    return render_template('register_page.html', current_date=current_date, current_time=current_time, info=info)

from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from flask_sqlalchemy import SQLAlchemy
#from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:M204816D@localhost/health_data' # my  local host database
#app.config['SQLALCHEMY_DATABASE_URI']='postgres://pcyfaiuedycvnn:69c1cc7e0eccf4604d324c91c4b9516657b85f661b2c5a069414aa6b3484ce7b@ec2-54-163-226-238.compute-1.amazonaws.com:5432/d2p4282r5d65nj?sslmode=require'
db=SQLAlchemy(app)


class Users(db.Model):
    __tablename__='registration Basalem'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text, unique=False)
    email=db.Column(db.Text, unique=True)
    username=db.Column(db.Text, unique=True)
    password=db.Column(db.Text, unique=False)

    def __init__(self,name,email,username,password):
        self.name=name
        self.email=email
        self.username=username
        self.password=password



class RegisterForm(Form):
    name=StringField('Name',[validators.length(min=1, max=50)])
    username=StringField('Username',[validators.length(min=4, max=25)])
    email=StringField('Email',[validators.length(min=6, max=50)])
    password=PasswordField('Password',[validators.DataRequired(),
    validators.EqualTo('confirm', message='Passwords do not match')])
    confirm=PasswordField('Confirm Password')
@app.route('/', methods=['GET', 'POST'])
def register():
    form=RegisterForm(request.form)
    if request.method=='POST' and form.validate():
        name= form.name.data
        email=form.email.data
        username=form.username.data
        password=sha256_crypt.encrypt(str(form.password.data))
        users=Users(name,email,username,password)
        db.session.add(users)
        db.session.commit()
        #flash('You are registered', 'success')
        #return redirect(url_for('main'))
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form["username"]
        password=request.form["password"]
        usernamecandidate=Users.query.filter_by(username=username).first()
        if usernamecandidate != None:
            if sha256_crypt.verify(password,usernamecandidate.password):
                print(" everything matched")
                session['logged']=True
                session['username']=username
                return redirect(url_for('panel'))
            else:
                print("****")
                error='wrong password'
                return render_template('login.html',error=error)
        else:
            error=' username not found'
            print("NONE matched")
            return render_template('login.html',error=error)
    return render_template('login.html')

def logged_in(s):
    @wraps(s)
    def wrap(*args, **kwargs):
        if 'logged' in session:
            return s(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/panel')
@logged_in
def panel():
    return render_template('panel.html')



if __name__== "__main__":
    app.secret_key='mohammed'
    app.debug=True
    app.run()

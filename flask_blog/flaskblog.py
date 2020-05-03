from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
import pymysql as sql
app = Flask(__name__)

"""import secrets
secrets.token_hex(16) 
"""
app.config['SECRET_KEY'] = '3d8135a995f6b988949bf4ef57971d2e'

posts = [
    {'author':'prateek',
    'title':'lord of the rings',
    'content':'content1',
    'date_posted':'april 27,2020'},

    {'author':'pratham',
    'title':'wings of fire',
    'content':'content2',
    'date_posted':'april 30,2020'},

    {'author':'piyush',
    'title':'hobbit',
    'content':'content3',
    'date_posted':'april 24,2020'}

]



@app.route("/")
@app.route("/home/")
def home():
    return render_template("home.html",posts=posts)

@app.route("/about/")
def about():
    return render_template("about.html",title = 'About')

@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'account created successfully for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('login successfullly', 'success')    
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

app.run(debug=True, host='localhost',port=80)
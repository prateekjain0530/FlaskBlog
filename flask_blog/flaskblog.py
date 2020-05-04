from flask import Flask, render_template, url_for, flash, redirect, session, request
from forms import RegistrationForm, LoginForm
import pymysql as sql
from datetime import datetime
from flask_bcrypt import Bcrypt
app = Flask(__name__)

"""import secrets
secrets.token_hex(16) 
"""
app.config['SECRET_KEY'] = '3d8135a995f6b988949bf4ef57971d2e'
db = sql.connect(host="localhost",port=3306,user="root",password='',database="user")

bcrypt = Bcrypt(app)

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
        c = db.cursor()
        c.execute("SELECT email,username FROM users where email='{}' or username='{}'".format(form.email.data,form.username.data))
        data = c.fetchone()
        if data:
            flash(f'email or username already exists for {form.email.data}!', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            
            cmd = "INSERT INTO users(username,email,password) values('{}','{}','{}')".format(form.username.data,form.email.data,hashed_password)
            c.execute(cmd)
            db.commit()
            flash(f'account created successfully for {form.username.data}!', 'success')
            return redirect(url_for('home'))
    
    return render_template('register.html', title='Register', form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    
    if request.cookies.get("email"):
        return render_template(url_for('home'))
    else:
        form = LoginForm() 
        if form.validate_on_submit():
            c = db.cursor()
            c.execute("SELECT * FROM users where email='{}'".format(form.email.data))
            data = c.fetchone()
            if bcrypt.check_password_hash(data[3], form.password.data):
                if form.remember.data:
                    session['email'] = form.email.data
                    #resp = make_response(render_template("one.html"))
                    #resp.set_cookie("email",email)
            #resp.set_cookie("islogin","true")
            #return resp
            #return "<h1>Email = {} and password = {}</h1>".format(email,password)
                flash('login successfullly', 'success')    
            return redirect(url_for('home'))
        return render_template('login.html', title='Login', form=form)

app.run(debug=True, host='localhost',port=80)
from flask import Flask, render_template, url_for, redirect, request, session
from pkg import app
from pkg.forms import LoginForm

#custom errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('page404.html')


#homepage
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

#about
@app.route('/Who we are')
def about():
    return render_template("about.html")

# #sign in
# @app.route('/sign in')
# def sign_in():
#     return render_template('login.html')

#blog
@app.route('/feed')
def feed():
    return render_template("feed.html")

#categories
@app.route('/categories')
def categories():
    return render_template("explore.html")

@app.route('/connect')
def connect():
    return render_template("connect.html")

@app.route('/profile')
def profile():
    if session.get('useremail') == None:
        return redirect('/login')
    else:
        return render_template("profile.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        useremail = form.userEmail.data
        password = form.userPassword.data
        session['useremail'] = useremail
        return redirect('/profile')

    return render_template('login.html', form=form)

        
@app.route('/logout')
def logout():
    session.pop('useremail', None)
    return redirect('/index')
    

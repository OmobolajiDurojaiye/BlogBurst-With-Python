from flask import Flask, render_template, url_for, redirect, request, session
from pkg import app

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

#sign in
@app.route('/sign in')
def sign_in():
    return render_template('login.html')

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        useremail = request.form.get('userEmail')
        password = request.form.get('userPassword')
        if useremail !="" and password != "":
            session['useremail']=useremail
            return redirect('/profile')
        else:
            return redirect('/login')

        
@app.route('/logout')
def logout():
    session.pop('useremail', None)
    return redirect('/index')
    

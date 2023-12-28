from flask import Flask, render_template, url_for, redirect, request, session
from pkg import app
from pkg.forms import LoginForm, RegistrationForm, BlogPostForm

#custom errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('page404.html')


#adminlogin
@app.route('/admin_login')
def admin_login():
    return render_template('adminlogin.html')

#admin
@app.route('/admin')
def admin():
    return render_template('admin.html')

#homepage
@app.route('/')
@app.route('/index')
def index():
    # return render_template("index.html")
    #since the modal is in index page, the form validator should be here
    form = RegistrationForm()

    if form.validate_on_submit():
        userfirstname = form.userfirstname.data
        userlastname = form.userlastname.data
        userregemail = form.userregemail.data
        userregpwd = form.userregpwd.data
        userdateofbirth = form.userdateofbirth.data
        usergender = form.usergender.data
        agree = form.agree.data

        session['username'] = userfirstname

        return redirect('/login')
    
    return render_template('index.html', form=form)

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
    
@app.route('/newpost', methods=['GET', 'POST'])
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        post_title = form.post_title.data
        post_image = form.post_image.data
        post_content = form.post_content.data

        session['title'] = post_title
        session['image'] = post_image
        session['content'] = post_content

        return render_template("feed.html", post_title=post_title, post_content=post_content, post_image=post_image)

    return render_template('newpost.html', form=form)
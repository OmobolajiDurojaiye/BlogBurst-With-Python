from flask import Flask, render_template, url_for, redirect, request, session
from pkg import app
from pkg.forms import LoginForm, RegistrationForm, BlogPostForm, AdminLoginForm, EditProfileForm

#custom errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('page404.html')


#adminlogin
@app.route('/admin_login/', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        session['adminusername'] = username

        return render_template('admin.html')
    
    return render_template('adminlogin.html', form=form)


#admin
@app.route('/admin/')
def admin():
    if session.get('adminusername') == None:
        return redirect('/admin_login/')
    else:
        return render_template("admin.html")

#adminlogout
@app.route('/adminlogout/')
def adminlogout():
    session.pop('adminusername', None)
    return redirect('/admin_login/')

#homepage
@app.route('/')
@app.route('/index/')
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

        return redirect('/login/')
    
    return render_template('index.html', form=form)


#about
@app.route('/Who we are/')
def about():
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

        return redirect('/login/')
    
    return render_template('about.html', form=form)

# #sign in
# @app.route('/sign in')
# def sign_in():
#     return render_template('login.html')


#blog
@app.route('/feed/', methods=['GET', 'POST'])
def feed():
    return render_template("feed.html")

#categories
@app.route('/categories/')
def categories():
    return render_template("explore.html")

#academic blogs
@app.route('/Academic Blogs/')
def academic_category():
    return render_template('academic_blogs.html')


#connect
@app.route('/connect/')
def connect():
    return render_template("connect.html")

#userprofile
@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    if session.get('useremail') is None:
        return redirect('/login/')
    
    form = EditProfileForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        bio = form.bio.data
        facebook = form.facebook.data
        instagram = form.instagram.data
        x = form.x.data
        email = form.email.data
        github = form.github.data

        return render_template('profile.html', form=form)

    return render_template('profile.html', form=form)

#Login 
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        useremail = form.userEmail.data
        password = form.userPassword.data
        session['useremail'] = useremail
        return redirect('/profile/')

    return render_template('login.html', form=form)


#Logout   
@app.route('/logout/')
def logout():
    session.pop('useremail', None)
    return redirect('/index/')
    
#add new post
@app.route('/newpost/', methods=['GET', 'POST'])
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        post_title = form.post_title.data
        post_image = form.post_image.data
        post_content = form.post_content.data
        post_description = form.post_description.data

        session['title'] = post_title
        session['image'] = post_image
        session['content'] = post_content
        session['description'] = post_description

        return render_template("feed.html", post_title=post_title, post_content=post_content, post_image=post_image,post_description=post_description)
    else:
        return render_template('newpost.html', form=form)
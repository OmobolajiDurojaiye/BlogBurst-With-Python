from flask import Flask, render_template, url_for, redirect, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app
from pkg.models import db, Post, User
from pkg.forms import LoginForm, RegistrationForm, BlogPostForm, AdminLoginForm, EditProfileForm

#custom errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('page404.html')


#homepage
@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    # return render_template("index.html")
    #since the modal is in index page, the form validator should be here
    form = RegistrationForm()

    if form.validate_on_submit():
        userfirstname = form.userfirstname.data
        userlastname = form.userlastname.data
        userregemail = form.userregemail.data
        userregpwd = form.userregpwd.data
        hashed_pwd = generate_password_hash(userregpwd)
        userdateofbirth = form.userdateofbirth.data
        usergender = form.usergender.data
        agree = form.agree.data

        user = User(user_fname=userfirstname, user_lname=userlastname, user_email=userregemail, user_password=hashed_pwd, user_date_of_birth=userdateofbirth, user_gender=usergender)

        db.session.add(user)
        db.session.commit()
        id = user.user_id
        session['useronline'] = id

        return redirect('/login/')
    
    return render_template('user/index.html', form=form)


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
    
    return render_template('user/about.html', form=form)

# #sign in
# @app.route('/sign in')
# def sign_in():
#     return render_template('login.html')


#blogs
@app.route('/feed/', methods=['GET', 'POST'])
def feed():
    posts = Post.query.order_by(Post.post_created_on.desc()).all() 
    return render_template("user/feed.html", posts=posts)

#categories
@app.route('/categories/')
def categories():
    return render_template("user/explore.html")

#academic blogs
@app.route('/categories/Academic Blogs/')
def academic_category():
    posts = Post.query.order_by(Post.post_created_on.desc()).all() 
    return render_template('user/academic_blogs.html', posts=posts)

#technical blogs
@app.route('/categories/Technical Blogs/')
def technical_category():
    return render_template('user/technical_blogs.html')

#creative blogs
@app.route('/categories/Creative Blogs/')
def creative_category():
    return render_template('user/creative_blogs.html')

#poetry blogs
@app.route('/categories/Poetic Blogs/')
def poetry_category():
    return render_template('user/poetic_blogs.html')

#journalistic blogs
@app.route('/categories/Journalistic Blogs/')
def journalistic_category():
    return render_template('user/journalistic_blogs.html')

#business blogs
@app.route('/categories/Business Blogs/')
def business_category():
    return render_template('user/business_blogs.html')

#Food and Recipe blogs
@app.route('/categories/Food-and-recipe Blogs/')
def Food_category():
    return render_template('user/Food-and-recipe_blogs.html')

#nature blogs
@app.route('/categories/Nature Blogs/')
def nature_category():
    return render_template('user/nature_blogs.html')

#humor blogs
@app.route('/categories/Humor Blogs/')
def humor_category():
    return render_template('user/humor_blogs.html')

#connect
@app.route('/connect/')
def connect():
    return render_template("user/connect.html")

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

        session['user_profilename'] = f"{first_name} {last_name}"

        return redirect('/profile/')

    return render_template('user/profile.html', form=form)

#Login 
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        useremail = form.userEmail.data
        password = form.userPassword.data
        session['useremail'] = useremail

        flash('You are now logged in')

        return redirect('/profile/')

    return render_template('user/login.html', form=form)


#Logout   
@app.route('/logout/')
def logout():
    session.pop('useremail', None)
    
    flash('You have been successfully logged out. Get back soon', 'danger')
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

        new_post = Post(post_title=post_title, post_image=post_image, post_content=post_content, post_description=post_description)
        db.session.add(new_post)
        db.session.commit()

        return redirect("/feed/")
    else:
        return render_template('user/newpost.html', form=form)


@app.route('/All Posts/')
def all_post():
    return render_template('user/all_posts.html')


#This's for testing 
# @app.route('/cat/')
# def cat():
#     return render_template('blogcategoriesbase.html')

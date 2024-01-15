import os, random, string
from functools import wraps
from flask import Flask, render_template, url_for, redirect, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app
from pkg.models import db, Post, User
from pkg.forms import LoginForm, RegistrationForm, BlogPostForm, EditProfileForm, UpdatePostForm

#custom errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('page404.html')


# homepage
@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()

    if form.validate_on_submit():
        fname = form.userfirstname.data
        lname = form.userlastname.data
        email = form.userregemail.data
        pwd = form.userregpwd.data
        hashed_pwd = generate_password_hash(pwd)
        dob = form.userdateofbirth.data
        gender = request.form.get('usergender')

        user = User(
            users_fname=fname,
            users_lname=lname,
            users_email=email,
            users_password=hashed_pwd,
            users_date_of_birth=dob,
            user_gender=gender
        )

        db.session.add(user)
        db.session.commit()

        session["useronline"] = user.users_id  # Make sure to use the correct primary key field

        return redirect('/index/')

    return render_template('user/index.html', form=form)    


#about
@app.route('/Who we are/')
def about():
    return render_template('user/about.html')

@app.route('/feed/', methods=['GET', 'POST'])
def feed():
    posts_with_writer_names = db.session.query(Post, User).join(User).order_by(Post.post_created_on.desc()).all()

    return render_template("user/feed.html", posts_with_writer_names=posts_with_writer_names)

#categories
@app.route('/categories/')
def categories():
    return render_template("user/explore.html")

#academic blogs
@app.route('/categories/Academic Blogs/')
def academic_category():
    posts = Post.query.all()
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


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    user_id = session.get('useronline')
    user = User.query.get(user_id)
    oldpix = user.users_profile_pic

    if user_id is None:
        flash('Please log in first', category='error')
        return redirect('/login')

    if user is None:
        flash('User not found', category='error')
        return redirect('/')

    form = EditProfileForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Retrieve form inputs from request
        first_name = form.first_name.data
        last_name = form.last_name.data
        bio = form.bio.data
        dp = request.files.get("dp")
        filename = dp.filename
        if filename == "":
            flash("Please select a file", category="error")
            return redirect("/changedp")
        else:
            name, ext = os.path.splitext(filename)
            allowed = ['.jpg', '.png', '.jpeg']
            if ext.lower() in allowed:
                final_name = str(int(random.random() * 100000)) + ext
                dp.save(f"pkg/static/uploads/{final_name}")
                user = User.query.get(user_id) 
                user.users_profile_pic = final_name
                db.session.commit()
                try:
                    os.remove(f"pkg/static/uploads/{oldpix}")
                except:
                    pass
                flash("Profile picture added", category='success')
                return redirect("/profile")

        # Update user profile information
        user.users_fname = first_name
        user.users_lname = last_name
        user.users_bio = bio
        user.users_profile_pic = filename

        db.session.commit()

        flash('Profile updated successfully', category='success')
        return redirect('/profile/')

    user_posts = Post.query.filter_by(post_writer=user_id).order_by(Post.post_created_on.desc()).all()

    return render_template('user/profile.html', form=form, user=user, user_posts=user_posts)



@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('user/login.html', form=form)
    else:
        if form.validate_on_submit():
            email = form.userEmail.data
            pwd = form.userPassword.data

            user = db.session.query(User).filter(User.users_email == email).first()
            if user:
                saved_pwd = user.users_password
                check = check_password_hash(saved_pwd, pwd)
                if check:
                    session['useronline'] = user.users_id
                    flash('Log in successful', category='success')
                    return redirect('/profile')
                else:
                    flash("Invalid credentials", category="error")
                    return redirect('/login/')
            else:
                flash("Invalid credentials", category="error")
                return redirect('/login/')
        else:
            return render_template('user/login.html', form=form)



#Logout   
@app.route('/logout/')
def logout():
    session.pop('useronline', None)
    
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

        user_id = session.get('useronline')

        if user_id is None:
            flash('Please log in first', category='error')
            return redirect('/login')
        else:
            new_post = Post(posts_title=post_title, posts_pic=post_image, posts_content=post_content, posts_description=post_description, post_writer=user_id)
            db.session.add(new_post)
            db.session.commit()

        return redirect("/feed/")
    else:
        return render_template('user/newpost.html', form=form)


@app.route('/All Posts/')
def all_post():
    user_id = session.get('useronline')
    user = User.query.get(user_id)
    user_posts = Post.query.filter_by(post_writer=user_id).order_by(Post.post_created_on.desc()).all()
    return render_template('user/all_posts.html', user_posts=user_posts, user=user)


# delete post
@app.route('/delete_post/<int:post_id>', methods=['POST', 'GET'])
def delete_post(post_id):
    user_id = session.get('useronline')
    post = Post.query.filter_by(posts_id=post_id, post_writer=user_id).first()

    if post:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully', 'success')
    else:
        flash('Post not found', 'error')

    return redirect(url_for('all_post'))


@app.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    user_id = session.get('useronline')
    post = Post.query.filter_by(posts_id=post_id, post_writer=user_id).first()

    if post:
        form = UpdatePostForm()

        if request.method == 'POST' and form.validate_on_submit():
            # Update the post with form data
            post.posts_title = form.updated_title.data
            post.posts_content = form.updated_content.data
            post.posts_description = form.updated_description.data

            # Commit the changes to the database
            db.session.commit()

            flash('Post updated successfully', 'success')
            return redirect(url_for('all_post'))

        return render_template('user/update_post.html', form=form, post=post)
    
    else:
        flash('Post not found or you do not have permission to update it', 'error')
        return redirect(url_for('all_post'))




#This's for testing 
# @app.route('/cat/')
# def cat():
#     return render_template('blogcategoriesbase.html')

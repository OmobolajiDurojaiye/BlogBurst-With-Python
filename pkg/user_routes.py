from datetime import datetime
import os, random, string
from functools import wraps
from sqlalchemy import func
from flask import Flask, render_template, url_for, redirect, request, session, flash, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app
from pkg.models import db, Post, User, Comment, Like, Announcement, Connection
from pkg.forms import LoginForm, RegistrationForm, BlogPostForm, EditProfileForm, UpdateBlogPostForm, CommentForm

#custom errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('page404.html')


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def deactivate_user_post(user_id):
    user = User.query.get(user_id)

    if user.is_active == False:
        posts = Post.query.filter_by(Post.posts_status)
        posts = 'Drafted'
        return redirect('/')

# homepage
@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.post_created_on.desc()).all()
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

        session["useronline"] = user.users_id  
        return redirect('/login/')

    return render_template('user/index.html', form=form, posts=posts)    


#about
@app.route('/Who-we-are/')
def about():
    return render_template('user/about.html')


#mistake mistake mistake, God whyyyyy??
# @app.route('/feed/', methods=['GET', 'POST'])
# def feed():
#     user_id = session.get('useronline')

#     if user_id is None:
#         flash('Please log in first', category='error')
#         return redirect('/login')

#     user = User.query.get(user_id)

#     if user.is_active is False:
#         flash("You've been disabled", category='error')
#         return redirect('/')

#     like = Like.query.count()
    
#     posts_with_writer_names = db.session.query(Post, User).join(User).order_by(Post.post_created_on.desc()).all()

#     form = CommentForm()

#     if form.validate_on_submit():
#         content = form.comment_content.data
#         post_id = request.form.get('post_id')

#         comment = Comment(comment_content=content, post_commented_on=post_id, user_commented=user_id)
#         db.session.add(comment)
#         db.session.commit()

#         flash('Your comment has been added successfully', 'success')
#         return redirect(url_for('feed'))

#     return render_template("user/feed.html", posts_with_writer_names=posts_with_writer_names, form=form, user=user, like=like)


@app.route('/feed/', methods=['GET', 'POST'])
def feed():
    user_id = session.get('useronline')
    user = User.query.get(user_id)

    if user_id is None:
        flash('Please log in first', category='error')
        return redirect('/login')

    if request.method == 'GET':
        like = Like.query.count()

        posts_with_writer_names = db.session.query(Post, User).join(User).order_by(Post.post_created_on.desc()).all()
        form = CommentForm()
        return render_template("user/feed.html", posts_with_writer_names=posts_with_writer_names, form=form, user=user, like=like)

    else:
        if user.is_active == False:
            flash("You've been disabled", category='error')
            return redirect('/')
    
        form = CommentForm()

        if form.validate_on_submit():
            content = form.comment_content.data
            post_id = request.form.get('post_id')

            comment = Comment(comment_content=content, post_commented_on=post_id, user_commented=user_id)
            db.session.add(comment)
            db.session.commit()

            flash('Your comment has been added successfully', 'success')
            return redirect(url_for('feed'))

        flash('Form validation failed', 'error')
        return redirect(url_for('feed'))




#categories
@app.route('/categories/')
def categories():
    user_id = session.get('useronline')
    user = User.query.get(user_id)

    if user.is_active == False:
        flash("You've been disabled", category='error')
        return redirect('/')
    else:
        return render_template("user/explore.html")

# academic blogs
@app.route('/categories/Academic/Blogs')
def academic_category():
    posts = Post.query.filter_by(posts_category='Academic').all()
    return render_template('user/academic_blogs.html', posts=posts)


#technical blogs
@app.route('/categories/Technical/Blogs/')
def technical_category():
    posts = Post.query.filter_by(posts_category='Technical').all()
    return render_template('user/technical_blogs.html', posts=posts)

#creative blogs
@app.route('/categories/Creative/Blogs/')
def creative_category():
    posts = Post.query.filter_by(posts_category='Creative').all()
    return render_template('user/creative_blogs.html', posts=posts)

#poetry blogs
@app.route('/categories/Poetic/Blogs/')
def poetry_category():
    posts = Post.query.filter_by(posts_category='Poetry').all()
    return render_template('user/poetic_blogs.html',posts=posts)

#journalistic blogs
@app.route('/categories/Journalistic/Blogs/')
def journalistic_category():
    posts = Post.query.filter_by(posts_category='Journalistic').all()
    return render_template('user/journalistic_blogs.html', posts=posts)

#business blogs
@app.route('/categories/Business/Blogs/')
def business_category():
    posts = Post.query.filter_by(posts_category='Business').all()
    return render_template('user/business_blogs.html', posts=posts)

#Food and Recipe blogs
@app.route('/categories/Food-and-recipe/Blogs/')
def Food_category():
    posts = Post.query.filter_by(posts_category='Food and Recipe').all()
    return render_template('user/Food-and-recipe_blogs.html',posts=posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):  # Change parameter name to post_id
    post = Post.query.get_or_404(post_id)
    return render_template('user/post_detail.html', post=post)


#nature blogs
@app.route('/categories/Nature/Blogs/')
def nature_category():
    posts = Post.query.filter_by(posts_category='Nature').all()
    return render_template('user/nature_blogs.html', posts=posts)

#humor blogs
@app.route('/categories/Humor/Blogs/')
def humor_category():
    posts = Post.query.filter_by(posts_category='Humor').all()
    return render_template('user/humor_blogs.html', posts=posts)

# # connect
# @app.route('/connect/')
# def connect():
#     user_id = session.get('useronline')
#     all_users = User.query.all()
#     if user_id == None:
#         flash('Please log in first', category='error')
#         return redirect('/login')
#     return render_template("user/connect.html", users=all_users)


def is_user_connected(user_one_id, user_two_id):
    connection = Connection.query.filter(
        ((Connection.user_one == user_one_id) & (Connection.user_two == user_two_id)) |
        ((Connection.user_one == user_two_id) & (Connection.user_two == user_one_id))
    ).first()

    return connection is not None


@app.route('/connect/')
def connect_all_users():
    current_user_id = session.get('useronline')

    if current_user_id is None:
        flash('Please log in first', category='error')
        return redirect('/login')

    all_users = User.query.filter(User.users_id != current_user_id, User.is_active == True).all()

    connection_status = {}

    for user in all_users:
        connection_status[user.users_id] = is_user_connected(current_user_id, user.users_id)

    return render_template("user/connect.html", users=all_users, current_user_id=current_user_id, connection_status=connection_status)




# # ...

# # New route to handle connection or disconnection actions
# @app.route('/connect/<int:user_id>/action', methods=['POST'])
# def handle_connection_action(user_id):
#     current_user_id = session.get('useronline')

#     # Check if the user is logged in
#     if current_user_id is None:
#         flash('Please log in first', category='error')
#         return redirect('/login')

#     # Check the action parameter to determine whether to connect or disconnect
#     action = request.form.get('action')

#     if action == 'connect':
#         # Connect the users
#         new_connection = Connection(user_one=current_user_id, user_two=user_id, date=datetime.utcnow())
#         db.session.add(new_connection)
#         db.session.commit()
#         flash('Connection successful', category='success')
#     elif action == 'disconnect':
#         # Disconnect the users
#         existing_connection = Connection.query.filter(
#             ((Connection.user_one == current_user_id) & (Connection.user_two == user_id)) |
#             ((Connection.user_one == user_id) & (Connection.user_two == current_user_id))
#         ).first()

#         if existing_connection:
#             db.session.delete(existing_connection)
#             db.session.commit()
#             flash('Disconnection successful', category='success')
#         else:
#             flash('No existing connection to disconnect', category='error')
#     else:
#         flash('Invalid action', category='error')

#     return redirect(url_for('connect_all_users'))



@app.route('/connect/<int:user_id>', methods=['POST'])
def connect(user_id):
    current_user_id = session.get('useronline')
    current_user = User.query.get(current_user_id)
    other_user = User.query.get(user_id)

    # This checks if users are already connected
    existing_connection = Connection.query.filter(
        ((Connection.user_one == current_user.users_id) & (Connection.user_two == other_user.users_id)) |
        ((Connection.user_one == other_user.users_id) & (Connection.user_two == current_user.users_id))
    ).first()

    if existing_connection:
        # Disconnect users
        db.session.delete(existing_connection)
        flash(f"You have disconnected with {other_user.users_fname}.", "success")
    else:
        # Connect users
        new_connection = Connection(user_one=current_user.users_id, user_two=other_user.users_id, date=datetime.utcnow().date())
        db.session.add(new_connection)
        flash(f"You are now connected with {other_user.users_fname}.", "success")

    db.session.commit()

    return redirect(url_for('connect_all_users'))




@app.route('/connections')
def connections():
    user_id = session.get('useronline')

    # Check if the user is logged in
    if user_id is None:
        flash('Please log in first', category='error')
        return redirect('/login')

    connections = Connection.query.filter(
        (Connection.user_one == user_id) | (Connection.user_two == user_id)
    ).all()

    connected_users = []
    for connection in connections:
        if connection.user_one != user_id:
            connected_users.append(User.query.get(connection.user_one))
        else:
            connected_users.append(User.query.get(connection.user_two))

    return render_template('user/connections.html', connected_users=connected_users)








# @app.route('/profile/', methods=['GET', 'POST'])
# def profile():
#     user_id = session.get('useronline')
#     user = User.query.get(user_id)

#     if user_id == None:
#         flash('Please log in first', category='error')
#         return redirect('/login')

#     if user == None:
#         flash('User not found', category='error')
#         return redirect('/')

#     form = EditProfileForm()

#     if request.method == 'POST':
#         if form.validate_on_submit():
#             first_name = form.first_name.data
#             last_name = form.last_name.data
#             bio = form.bio.data
#             facebook = form.facebook.data
#             instagram = form.instagram.data
#             x = form.x.data
#             github = form.github.data 
#             gmail = form.email.data

#             user.users_fname = first_name
#             user.users_lname = last_name
#             user.users_bio = bio
#             user.facebook_url = facebook
#             user.instagram_url = instagram
#             user.x_url = x
#             user.github_url = github  
#             user.gmail_url = gmail
#             db.session.add(user)
#             db.session.commit()
#             flash('Profile updated successfully', category='success')
#             return redirect('/profile/')
        
#         db.session.commit()
#         flash('Profile updated successfully', category='success')
#             # return redirect('/profile/')

#         dp = request.files.get("dp")

#         if dp and dp.filename != "":

#             filename = dp.filename 
#             name, ext = os.path.splitext(filename)
#             allowed = ['.jpg', '.png', '.jpeg']
            
#             if ext.lower() in allowed:
#                 final_name = str(int(random.random() * 100000)) + ext
#                 dp.save(f"pkg/static/uploads/{final_name}")

#                 user.users_profile_pic = final_name
#                 db.session.commit()
#                 flash("Profile picture added", category='success')
#             else:
#                 flash("Invalid file type. Please upload a valid image.", category="error")


#     user_posts = Post.query.filter_by(post_writer=user_id).order_by(Post.post_created_on.desc()).all()

#     return render_template('user/profile.html', form=form, user=user, user_posts=user_posts)  


@app.route('/changedp/', methods=['GET', 'POST'])
def change_dp():
    user_id = session.get('useronline')
    user = User.query.get(user_id)

    if user_id is None:
        flash('Please log in first', category='error')
        return redirect('/login')

    if user is None:
        flash('User not found', category='error')
        return redirect('/')

    if request.method == 'POST':
        oldpix = user.users_profile_pic
        dp = request.files.get("dp")

        if dp and dp.filename != "":
            filename = dp.filename 
            name, ext = os.path.splitext(filename)
            allowed = ['.jpg', '.png', '.jpeg']
            
            if ext.lower() in allowed:
                final_name = str(int(random.random() * 100000)) + ext
                dp.save(os.path.join("pkg/static/uploads/", final_name))

                user.users_profile_pic = final_name
                db.session.commit()

                try:
                    os.remove(f"pkg/static/uploads/{oldpix}")
                except:
                    pass

                flash("Profile picture added", category='success')
                return redirect(url_for('profile')) 
            else:
                flash("Invalid file type. Please upload a valid image.", category="error")

    return render_template('user/profile.html')


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    user_id = session.get('useronline')
    user = User.query.get(user_id)

    if user is None:
        flash('User not found', category='error')
        return redirect('/')

    if user.is_active is False:
        flash("Your account has been disabled", category='error')
        return redirect('/')

    if user_id is None:
        flash('Please log in first', category='error')
        return redirect('/login')

    form = EditProfileForm()

    announcements = Announcement.query.all()

    if request.method == 'POST':
        if form.validate_on_submit():
            user.users_fname = form.first_name.data
            user.users_lname = form.last_name.data
            user.users_bio = form.bio.data
            user.facebook_url = form.facebook.data
            user.instagram_url = form.instagram.data
            user.x_url = form.x.data
            user.github_url = form.github.data
            user.gmail_url = form.email.data

            db.session.commit()
            flash('Profile updated successfully', category='error')
            return redirect('/profile/')
            
        else:
            flash("Invalid", category='error')
            return redirect('/profile/')
    else:
        form.first_name.data = user.users_fname
        form.last_name.data = user.users_lname
        form.bio.data = user.users_bio
        form.facebook.data = user.facebook_url
        form.instagram.data = user.instagram_url
        form.x.data = user.x_url
        form.github.data = user.github_url
        form.email.data = user.gmail_url
        user_posts = Post.query.filter_by(post_writer=user_id).order_by(Post.post_created_on.desc()).all()

        return render_template('user/profile.html', form=form, user=user, user_posts=user_posts, announcements=announcements)




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
                if user.is_active is False:
                    flash("You've been disabled", category='error')
                    return redirect('/')
                else:
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
    return redirect('/login/')
    
# #add new post
# @app.route('/newpost/', methods=['GET', 'POST'])
# def create_post():
#     form = BlogPostForm()

#     if form.validate_on_submit():
#         post_title = form.post_title.data
#         post_image = form.post_image.data
#         post_content = form.post_content.data
#         post_description = form.post_description.data
#         post_status = form.status.data
#         post_category = form.categories.data

#         user_id = session.get('useronline')

#         if user_id is None:
#             flash('Please log in first', category='error')
#             return redirect('/login')
#         else:
#             new_post = Post(
#                 posts_title=post_title,
#                 posts_pic=post_image,
#                 posts_content=post_content,
#                 posts_description=post_description,
#                 post_writer=user_id,
#                 posts_status=post_status,
#                 posts_category=post_category
#             )
#             db.session.add(new_post)
#             db.session.commit()

#         return redirect("/feed/")
#     else:
#         return render_template('user/newpost.html', form=form)



@app.route('/newpost/', methods=['GET', 'POST'])
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        post_title = form.post_title.data
        post_content = form.post_content.data
        post_description = form.post_description.data
        post_status = form.status.data
        post_category = form.categories.data

        user_id = session.get('useronline')

        if user_id is None:
            flash('Please log in first', category='error')
            return redirect('/login')
        
        if 'post_image' in request.files:
            post_image = request.files['post_image']
            
            if post_image and allowed_file(post_image.filename):
                filename = secure_filename(post_image.filename)
                
                final_name = os.path.join("pkg/static/postsimgs/", filename)
                post_image.save(final_name)

                new_post = Post(
                    posts_title=post_title,
                    posts_pic=filename,  
                    posts_content=post_content,
                    posts_description=post_description,
                    post_writer=user_id,
                    posts_status=post_status,
                    posts_category=post_category
                )

                db.session.add(new_post)
                db.session.commit()

                return redirect("/feed/")
            else:
                flash('Invalid file type. Please upload a valid image (jpg, jpeg, or png).', category='error')
                return redirect(request.url)

    return render_template('user/newpost.html', form=form)





@app.route('/all_posts/')
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
        Like.query.filter_by(post_liked=post.posts_id).delete()
        Comment.query.filter_by(post_commented_on=post.posts_id).delete()

        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully', 'success')
    else:
        flash('Post not found', 'error')

    return redirect(url_for('all_post'))


@app.route('/updatepost/<int:post_id>/', methods=['GET', 'POST'])
def update_post(post_id):
    form = UpdateBlogPostForm()

    post = Post.query.get_or_404(post_id)

    if request.method == 'POST' and form.validate_on_submit():
        post.posts_title = form.updated_title.data
        post.posts_description = form.updated_description.data
        post.posts_content = form.updated_content.data
        post.posts_status = request.form.get('status')

        db.session.commit()

        flash('Your post has been updated successfully!', 'success')
        return redirect("/feed/")

    form.updated_title.data = post.posts_title
    form.updated_description.data = post.posts_description
    form.updated_content.data = post.posts_content

    return render_template('user/update_post.html', form=form, post=post)




@app.route('/terms-and-conditions/')
def terms_conditions():
    return render_template('user/terms_condition.html')



# @app.route('/user_profile/<int:user_id>')
# def user_profile(user_id):
#     user = User.query.get(user_id)
#     posts = Post.query.filter_by(post_writer=user_id).all()

    return render_template('user/profile_page.html', user=user, posts=posts)


@app.route('/user_profile/<int:user_id>')
def user_profile(user_id):
    user = User.query.get(user_id)
    posts = Post.query.filter_by(post_writer=user_id).all()

    if user.is_active is False:
        flash("User has been disabled", category='error')
        return redirect('/profile')
    

    connections = Connection.query.filter(
        (Connection.user_one == user_id) | (Connection.user_two == user_id)
    ).all()

    connected_users = []
    for connection in connections:
        connected_user_id = connection.user_one if connection.user_one != user_id else connection.user_two
        connected_user = User.query.get(connected_user_id)
        connected_users.append(connected_user)

    return render_template('user/profile_page.html', user=user, posts=posts, connected_users=connected_users)





# @app.route('/json/like/', methods=['POST'])
# def like():
#     try:
#         user_id = session.get('useronline')

#         if user_id is None:
#             return jsonify({'error': 'User not logged in'}), 401 
        
#         if request.method == 'POST':
#             postId = request.form.get("postId")
#             likeCounts = request.form.get("likeCounts")

#             existing_like = Like.query.filter_by(post_liked=postId, user_id=user_id).first()
            
#             post = Post.query.get(postId)
#             post.posts_likes = likeCounts

#             new_like = Like(post_liked=postId, user_id=user_id)  
#             db.session.add(new_like)

#             db.session.commit()

#             return ""

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({'error': 'An error occurred during the like process', 'details': str(e)}), 500




@app.route('/json/like/', methods=['POST'])
def like():
    try:
        user_id = session.get('useronline')

        if user_id is None:
            return 'User not logged in', 401

        if request.method == 'POST':
            post_id = request.form.get("postId")
            like_count = int(request.form.get("likeCount"))

            existing_like = Like.query.filter_by(post_liked=post_id, user_id=user_id).first()

            if existing_like:
                db.session.delete(existing_like)
                like_count -= 1
            else:
                new_like = Like(post_liked=post_id, user_id=user_id)
                db.session.add(new_like)
                like_count += 1

            post = Post.query.get(post_id)
            post.posts_likes = like_count

            db.session.commit()

            return f'Like updated successfully, new like count: {like_count}'

    except Exception as e:
        print(f"Error: {str(e)}")
        return f'An error occurred during the like process: {str(e)}', 500
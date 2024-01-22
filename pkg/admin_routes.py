from flask import Flask, render_template, url_for, redirect, request, session, flash
from pkg import app
from pkg.models import db, Admin, User, Post, Comment, Like
from pkg.forms import AdminLoginForm
from werkzeug.security import generate_password_hash, check_password_hash
#custom errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('page404.html')


# admin login
@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()

    if request.method == 'GET':
        if session.get('adminonline') is None:
            return render_template('admin/adminlogin.html', form=form)
    else:
        admin_username = form.username.data.casefold()
        admin_password = form.password.data
        admin = db.session.query(Admin).filter(Admin.admin_username == admin_username).first()
        if admin is not None:
            if 'adminonline' not in session:
                # Password is not hashed in the database, check it without hashing
                if admin_password == admin.admin_password:
                    session['adminonline'] = admin.admin_id
                    return redirect('/admin/')
                else:
                    flash("Invalid credentials", category="error")
                    return redirect('/admin/login/')
            else:
                flash("Already logged in", category="info")
                return redirect('/admin/')
        else:
            flash("Invalid credentials", category="error")
            return redirect('/admin/login/')




#admin
@app.route('/admin/')
def admin():
    users = User.query.all()
    posts = Post.query.all()

    return render_template('admin/admin.html', users=users, user_count=len(users), posts=posts, post_count=len(posts))

#adminlogout
@app.route('/adminlogout/')
def adminlogout():
    session.pop('adminonline', None)
    return redirect('/admin/login/')


@app.route('/admin/user_management/')
def user_management():
    users = User.query.all()

    # Create a list to store user data with associated posts
    user_data = []

    for user in users:
        # Fetch posts for each user
        posts = Post.query.filter_by(post_writer=user.users_id).all()

        # Append user data with posts to the user_data list
        user_data.append({'user': user, 'posts': posts})

    return render_template('admin/user_management.html', user_data=user_data)



@app.route('/admin/delete_user/<int:user_id>', methods=['POST', 'GET'])
def admin_delete_user(user_id):
    if request.method == 'GET':
        flash("Can't delete!", 'error')
        return redirect(url_for('user_management'))

    user = User.query.get(user_id)
    if user:
        # Delete associated posts first
        posts = Post.query.filter_by(post_writer=user_id).all()
        for post in posts:
            # Delete associated comments first
            comments = Comment.query.filter_by(post_commented_on=post.posts_id).all()
            for comment in comments:
                db.session.delete(comment)

            db.session.delete(post)

        db.session.delete(user)
        db.session.commit()
        flash('User and associated posts/comments deleted successfully!', 'success')
    else:
        flash('User not found!', 'error')
    return redirect(url_for('user_management'))



@app.route('/admin/delete_post/<int:post_id>', methods=['POST', 'GET'])
def admin_delete_post(post_id):
    if request.method == 'GET':
        flash('Invalid method. Use POST to delete a post.', 'error')
        return redirect(url_for('user_management'))

    post = Post.query.get(post_id)
    if post:
        # Delete associated comments first
        comments = Comment.query.filter_by(post_commented_on=post_id).all()
        for comment in comments:
            db.session.delete(comment)

        db.session.delete(post)
        db.session.commit()
        flash('Post and associated comments deleted successfully!', 'success')
    else:
        flash('Post not found!', 'error')
    
    return redirect(url_for('user_management'))


@app.route('/admin/delete_all_posts/<int:user_id>', methods=['POST', 'GET'])
def delete_all_posts(user_id):
    if request.method == 'GET':
        flash('Invalid method. Use POST to delete all posts for a user.', 'error')
        return redirect(url_for('user_management'))

    # Delete all posts for the given user_id
    posts = Post.query.filter_by(post_writer=user_id).all()
    for post in posts:
        # Delete associated comments first
        comments = Comment.query.filter_by(post_commented_on=post.posts_id).all()
        for comment in comments:
            db.session.delete(comment)

        # Delete associated likes
        likes = Like.query.filter_by(post_liked=post.posts_id).all()
        for like in likes:
            db.session.delete(like)

        db.session.delete(post)

    # Commit changes to the database
    db.session.commit()

    flash('All posts and associated comments and likes have been deleted.', 'success')
    return redirect(url_for('user_management'))

@app.route('/admin/disable_post/<int:post_id>', methods=['POST'])
def admin_disable_post(post_id):
    post = Post.query.get(post_id)
    if post:
        # Update the post status to "Disabled"
        post.posts_status = 'Disabled'
        post.re_enable_allowed = False  # Disallow re-enabling
        db.session.commit()
        flash('Post disabled successfully!', 'success')
    else:
        flash('Post not found!', 'error')

    return redirect(url_for('user_management'))

# Example route for enabling a post
@app.route('/enable_post/<int:post_id>', methods=['POST'])
def enable_post(post_id):
    post = Post.query.get(post_id)
    if post:
        if post.re_enable_allowed == False:
            post.posts_status = 'Approved' 
            db.session.commit()
            flash('Post re-enabled successfully!', 'success')
        else:
            flash('Re-enabling this post is not allowed.', 'error')
    else:
        flash('Post not found!', 'error')

    return redirect(url_for('user_management'))



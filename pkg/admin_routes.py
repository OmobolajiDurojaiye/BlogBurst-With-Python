from flask import Flask, render_template, url_for, redirect, request, session, flash
from pkg import app, mail
from pkg.models import db, Admin, User, Post, Comment, Like, Announcement, Connection
from pkg.forms import AdminLoginForm, AnnouncementForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
#custom errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('page404.html')

def enable_user_posts(user):
    user_posts = Post.query.filter_by(post_writer=user.users_id, posts_status='Drafted').all()
    for post in user_posts:
        post.posts_status = 'Approved'
    db.session.commit()



@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()

    if request.method == 'GET':
        return render_template('admin/adminlogin.html', form=form)
    else:
        admin_username = form.username.data
        admin_password = form.password.data
        admin = db.session.query(Admin).filter(Admin.admin_username == admin_username).first()
        if admin and admin_password == admin.admin_password:
            session['adminonline'] = admin.admin_id
            flash("Welcome", category="success")
            return redirect('/admin/')
        else:
            flash("Invalid credentials", category="error")
            return redirect('/admin/login/')

# admin
@app.route('/admin/')
def admin():
    users = User.query.all()
    posts = Post.query.all()
    id = session.get('adminonline')

    if id is None: 
        return redirect('/admin/login/')  

    return render_template('admin/admin.html', users=users, user_count=len(users), posts=posts, post_count=len(posts))

# adminlogout
@app.route('/adminlogout/')
def adminlogout():
    session.pop('adminonline', None)
    return redirect('/admin/login/')



@app.route('/admin/user_management/')
def user_management():
    
    users = User.query.all()

    user_data = []

    for user in users:
        posts = Post.query.filter_by(post_writer=user.users_id).all()

        user_data.append({'user': user, 'posts': posts})

    return render_template('admin/user_management.html', user_data=user_data)



# @app.route('/admin/delete_user/<int:user_id>', methods=['POST', 'GET'])
# def admin_delete_user(user_id):
#     if request.method == 'GET':
#         flash("Can't delete!", 'error')
#         return redirect(url_for('user_management'))

#     user = User.query.get(user_id)
#     if user:
#         # Delete associated posts first
#         posts = Post.query.filter_by(post_writer=user_id).all()
#         for post in posts:
#             # Delete associated comments first
#             comments = Comment.query.filter_by(post_commented_on=post.posts_id).all()
#             for comment in comments:
#                 db.session.delete(comment)

#             db.session.delete(post)

#         db.session.delete(user)
#         db.session.commit()
#         flash('User and associated posts/comments deleted successfully!', 'success')
#     else:
#         flash('User not found!', 'error')
#     return redirect(url_for('user_management'))


@app.route('/admin/delete_user/<int:user_id>', methods=['POST', 'GET'])
def admin_delete_user(user_id):
    if request.method == 'GET':
        flash("Can't delete!", 'error')
        return redirect(url_for('user_management'))

    user = User.query.get(user_id)
    if user:
        if user.is_active:
            connections_to_delete = Connection.query.filter((Connection.user_one == user_id) | (Connection.user_two == user_id)).all()
            for connection in connections_to_delete:
                db.session.delete(connection)

            posts = Post.query.filter_by(post_writer=user_id).all()
            for post in posts:
                comments = Comment.query.filter_by(post_commented_on=post.posts_id).all()
                for comment in comments:
                    db.session.delete(comment)

                db.session.delete(post)

            db.session.delete(user)
            db.session.commit()
            flash('User and associated posts/comments/connections deleted successfully!', 'success')
        else:
            flash('User account is already disabled!', 'error')
    else:
        flash('User account does not exist or has been deleted!', 'error')

    return redirect(url_for('user_management'))


@app.route('/admin/disable_user/<int:user_id>', methods=['POST'])
def admin_disable_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        if user:
            #diable the user
            user.is_active = False
            db.session.commit()
            flash('User disabled successfully!', 'success')

            # Draft the user's posts
            user_posts = Post.query.filter_by(post_writer=user.users_id, posts_status='Approved').all()
            for post in user_posts:
                post.posts_status = 'Disabled'
            db.session.commit()

        else:
            flash('User account does not exist or has been deleted!', 'error')

        return redirect(url_for('user_management'))
    else:
        return render_template('admin/user_management.html', user=user)
    
    

@app.route('/admin/enable_user/<int:user_id>', methods=['POST', 'GET'])
def admin_enable_user(user_id):
    user = User.query.get(user_id)

    if request.method == 'POST':

        if user:
            user.is_active = True
            db.session.commit()
            flash('User enabled successfully!', 'success')

            enable_user_posts(user)
        else:
            flash('User account does not exist or has been deleted!', 'error')
        
        return redirect(url_for('user_management'))
    else:
        return render_template('admin/user_management.html', user=user)




@app.route('/admin/delete_post/<int:post_id>', methods=['POST', 'GET'])
def admin_delete_post(post_id):
    if request.method == 'GET':
        flash('Invalid method. Use POST to delete a post.', 'error')
        return redirect(url_for('user_management'))

    post = Post.query.get(post_id)
    if post:
        # Delete all associated comments first
        comments = Comment.query.filter_by(post_commented_on=post_id).all()
        for comment in comments:
            db.session.delete(comment)

        # Delete associated likes
        likes = Like.query.filter_by(post_liked=post_id).all()
        for like in likes:
            db.session.delete(like)

        db.session.delete(post)
        db.session.commit()
        flash('Post and associated comments/likes deleted successfully!', 'success')
    else:
        flash('Post not found!', 'error')
    
    return redirect(url_for('user_management'))


@app.route('/admin/delete_all_posts/<int:user_id>', methods=['POST', 'GET'])
def delete_all_posts(user_id):
    if request.method == 'GET':
        flash('Invalid method. Use POST to delete all posts for a user.', 'error')
        return redirect(url_for('user_management'))

    posts = Post.query.filter_by(post_writer=user_id).all()
    for post in posts:
        comments = Comment.query.filter_by(post_commented_on=post.posts_id).all()
        for comment in comments:
            db.session.delete(comment)

        likes = Like.query.filter_by(post_liked=post.posts_id).all()
        for like in likes:
            db.session.delete(like)

        db.session.delete(post)

    db.session.commit()

    flash('All posts and associated comments and likes have been deleted.', 'success')
    return redirect(url_for('user_management'))

@app.route('/admin/disable_post/<int:post_id>', methods=['POST'])
def admin_disable_post(post_id):
    post = Post.query.get(post_id)
    if post:
        post.posts_status = 'Disabled'
        # post.re_enable_allowed = False  # Disallow re-enabling
        db.session.commit()
        flash('Post disabled successfully!', 'success')
    else:
        flash('Post not found!', 'error')

    return redirect(url_for('user_management'))

# # Example route for enabling a post
# @app.route('/enable_post/<int:post_id>', methods=['POST'])
# def enable_post(post_id):
#     post = Post.query.get(post_id)
#     if post:
#         post.posts_status = 'Approved' 
#         db.session.commit()
#         flash('Post re-enabled successfully!', 'success')
#     else:
#         flash('Post not found!', 'error')

#     return redirect(url_for('user_management'))

@app.route('/enable_post/<int:post_id>', methods=['POST'])
def enable_post(post_id):
    post = Post.query.get(post_id)
    if post:
        post.posts_status = 'Approved'
        db.session.commit()
        flash('Post re-enabled successfully!', 'success')
    else:
        flash('Post not found!', 'error')

    return redirect(url_for('user_management'))



# @app.route('/admin/announcements/', methods=['GET', 'POST'])
# def admin_announcements():
#     online = session.get('adminonline')
#     form = AnnouncementForm()

#     if online:

#         if form.validate_on_submit():
#             new_announcement = Announcement(
#                 admin_id=session.get('adminonline'),
#                 message=form.message.data
#             )
#             db.session.add(new_announcement)
#             db.session.commit()
#             flash('Announcement created successfully', 'success')
#             return redirect(url_for('admin_announcements'))

#         announcements = Announcement.query.all()
#         return render_template('admin/announcement.html', form=form, announcements=announcements)
#     else:
#         return redirect('/admin/login/')


#with this, users can now receive email announcement
@app.route('/admin/announcements/', methods=['GET', 'POST'])
def admin_announcements():
    online = session.get('adminonline')
    form = AnnouncementForm()

    if online:
        if form.validate_on_submit():
            new_announcement = Announcement(
                admin_id=session.get('adminonline'),
                message=form.message.data
            )
            db.session.add(new_announcement)
            db.session.commit()

            all_users = User.query.all()

            for user in all_users:
                subject = 'New Message from BlogBurst admin'
                body = f"""
                    <html>
                        <head>
                            <style>
                                body {{
                                    color: white;
                                }}
                            </style>
                        </head>
                        <body>
                            <h1 style="background-color: plum; border-radius: 20px; padding: 20px; color: white;">{subject}</h1>
                            <p style="text-align: left; line-spacing: 2px;">{form.message.data}</p>
                        </body>
                    </html>
                """
                msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[user.users_email])
                msg.html = body
                mail.send(msg)

            flash('Announcement created successfully', 'success')
            return redirect(url_for('admin_announcements'))

        announcements = Announcement.query.all()
        return render_template('admin/announcement.html', form=form, announcements=announcements)
    else:
        return redirect('/admin/login/')

@app.route('/admin/announcements/delete/<int:id>', methods=['POST'])
def delete_announcement(id):
    announcement = Announcement.query.get_or_404(id)
    db.session.delete(announcement)
    db.session.commit()
    flash('Announcement deleted successfully', 'success')
    return redirect(url_for('admin_announcements'))

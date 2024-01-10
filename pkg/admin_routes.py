from flask import Flask, render_template, url_for, redirect, request, session, flash
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

        return render_template('admin/admin.html')
    
    return render_template('admin/adminlogin.html', form=form)


#admin
@app.route('/admin/')
def admin():
    if session.get('adminusername') == None:
        return redirect('/admin_login/')
    else:
        return render_template("admin/admin.html")

#adminlogout
@app.route('/adminlogout/')
def adminlogout():
    session.pop('adminusername', None)
    return redirect('/admin_login/')
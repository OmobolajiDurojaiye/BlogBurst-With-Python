from flask import Flask, render_template, url_for, redirect, request, session, flash
from pkg import app
from pkg.models import db,User
from pkg.forms import AdminLoginForm
from werkzeug.security import generate_password_hash, check_password_hash
#custom errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('page404.html')


#adminlogin
@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()

    if request.method == 'GET':
        return render_template('admin/adminlogin.html', form=form)
    else:
        admin_username =form.username.data.title()
        admin_password = form.password.data 
        admin = db.session.query(User).filter(User.users_fname == admin_username).first()
        if admin != None and admin.users_fname.lower() == "blogburst":
            saved_pwd = admin.users_password
            check =  check_password_hash(saved_pwd, admin_password)
            if check:
                session['adminonline'] = admin.users_id
                return redirect('/admin/')
            else:
                flash("Invalid credentials", category="error")
                return redirect('/admin/login/')
        else:
            flash("Invalid credentials", category="error")
            return redirect('/admin/login/')




#admin
@app.route('/admin/')
def admin():
    return render_template('admin/admin.html')

#adminlogout
@app.route('/adminlogout/')
def adminlogout():
    session.pop('adminonline', None)
    return redirect('/admin/login/')
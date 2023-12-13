from flask import render_template, request, redirect, session, flash
from app_flask.models.users_models import User
from app_flask import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def login_and_register():
    return render_template("register_and_login.html")

@app.route("/process/register", methods=['POST'])
def process_register():
    if User.validate_register(request.form) == False:
        return redirect("/")
    encrypted_password = bcrypt.generate_password_hash(request.form['password'])
    new_user = {
        **request.form,
        'password' : encrypted_password
    }
    user_id = User.create_one(new_user)
    session['user_id'] = user_id
    session['first_name'] = new_user['first_name']
    session['last_name'] = new_user['last_name']
    
    return redirect ("/dashboard")

@app.route("/process/login", methods=['POST'])
def process_login():
    user_login = User.obtain_one(request.form)
    if user_login == None:
        flash("This email doesn't exist", 'login_error')
        return redirect("/")
    if not bcrypt.check_password_hash(user_login.password, request.form['password']):
        flash('The password entered is incorrect', 'login_error')
        return redirect("/")
    session['user_id'] = user_login.id
    session['first_name'] = user_login.first_name
    session['last_name'] = user_login.last_name
    return redirect("/dashboard")

@app.route("/process/logout", methods=['POST'])
def logout():
    session.clear()
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("dashboard.html")
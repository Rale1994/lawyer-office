from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from users.forms import RegistrationForm, LoginForm, UpdateAccount
from blog import app, db, bcrypt, login_manager
from werkzeug.security import generate_password_hash
from blog.models import User
from users.helper import save_picture

users = Blueprint("users", __name__)


@users.route("/registration", methods=["POST", "GET"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256',
        #                                              salt_length=8)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        new_user = User(name=form.name.data, password=hashed_password, email=form.email.data)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users.login'))

    return render_template("registration.html", form=form, title="Registration form")


@users.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return render_template("home.html")

        if not user:
            return redirect(url_for('users.login'))

    return render_template('login.html', form=form, title="Log in")


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email

    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template("account.html", title="My account", form=form, image_file=image_file)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

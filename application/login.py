from application import project, db
from application.forms import LoginForm, RegisterForm
from application.models import UserLogin, Venue
from flask import render_template, url_for, redirect
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt


login_manager = LoginManager()
login_manager.init_app(project)
login_manager.login_view = "login"

bcrypt = Bcrypt(project)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin.query.get(int(user_id))


@project.route('/')
def index():  # put application's code her
    return render_template("index.html")


@project.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserLogin.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('userdashb'))
    return render_template("login.html", form=form)


@project.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = UserLogin(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


@project.route('/userdashb', methods=('GET', 'POST'))
@login_required
def userdashb():
    venues = Venue.query.order_by(Venue.venueid)
    return render_template("userdashb.html", venues=venues)


@project.route('/adminlogin', methods=('GET', 'POST'))
def adminlogin():
    form = LoginForm()
    if form.validate_on_submit():
        user1 = form.username.data
        if user1 == 'admin123':
            user = UserLogin.query.filter_by(username=user1).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('admindb'))

    return render_template("adminlogin.html", form=form)

@project.route('/admindb', methods=('GET', 'POST'))
@login_required
def admindb():
    venues = Venue.query.order_by(Venue.venueid)
    return render_template("admindb.html", venues=venues)

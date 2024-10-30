from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from models.users import Users
from models.login import LoginForm
from models.engine.database import session
from werkzeug.security import check_password_hash
from dotenv import load_dotenv

load_dotenv()

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/', strict_slashes=False, methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = session.query(Users).filter_by(username=form.username.data).first()

            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home.index'))
            else:
                flash('Invalid username or password', 'error')

        except Exception as e:
            flash(f'An error occurred while processing your request: {str(e)}', 'error')
            session.rollback()
        
        finally:
            session.close()

    return render_template('landing.html', form=form)



@landing_bp.route('/logout', strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for('landing.login'))


@landing_bp.route("/denied_access", strict_slashes=False)
def denied_access():
    return render_template("denied_access.html")

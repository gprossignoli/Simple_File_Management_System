from flask import Blueprint
from flask_login import logout_user
from werkzeug.utils import redirect

from sfms import UserManager

users = Blueprint(name='users', import_name=__name__)


@users.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return redirect("/home")

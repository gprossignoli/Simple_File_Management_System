from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager

from sfms import settings as st


app = Flask(__name__)
app.config['SECRET_KEY'] = st.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{st.DB_NAME}.db'
app.config['CSRF_ENABLED'] = st.CSRF
app.config['USER_APP_NAME'] = st.USER_APP_NAME
app.config['USER_ENABLE_EMAIL'] = st.USER_ENABLE_EMAIL
app.config['USER_ENABLE_USERNAME'] = st.USER_ENABLE_USERNAME

db = SQLAlchemy(app)
from sfms.main.routes import main
from sfms.files.routes import files
from sfms.users.routes import users
app.register_blueprint(blueprint=main)
app.register_blueprint(blueprint=files)
app.register_blueprint(blueprint=users)
from sfms.users.models import User
UserManager(app, db, User)
db.create_all()

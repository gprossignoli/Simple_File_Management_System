from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from sfms import settings as st

app = Flask(__name__)
app.config['SECRET_KEY'] = st.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite//:{st.DB_NAME}.db'
app.config['CSRF_ENABLED'] = st.CSRF
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


@app.route("/home", methods=['GET'])
def home():
    return render_template('home.html')


from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    file = FileField()
    submit = SubmitField('Submit')

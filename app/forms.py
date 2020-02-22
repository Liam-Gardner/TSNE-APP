from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, FormField, FieldList
from flask_wtf.file import FileField, FileRequired


class UploadDataFile(FlaskForm):
    file = FileField("Upload .csv file", validators=[FileRequired()])


class CheckForm(FlaskForm):
    submit = SubmitField("Submit")


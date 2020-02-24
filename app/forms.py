from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    SubmitField,
    FormField,
    FieldList,
    StringField,
    IntegerField,
)
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired


class UploadDataFile(FlaskForm):
    file = FileField("Upload .csv file", validators=[FileRequired()])


class CheckForm(FlaskForm):
    submit = SubmitField("Submit")


class SubsetForm(FlaskForm):
    subsetName = StringField("Subset Name", render_kw={"placeholder": "Subset Name"},)
    submit = SubmitField("Submit")


class RedirectFormElbow(FlaskForm):
    submit = SubmitField("Elbow Plot")


class RedirectFormTSNE(FlaskForm):
    perplexity = IntegerField(
        "Perplexity", render_kw={"placeholder": "Set perplexity..."},
    )
    iterations = IntegerField(
        "Iterations", render_kw={"placeholder": "Set iterations..."},
    )
    submit = SubmitField("TSNE Plot")


class ClusterNumberForm(FlaskForm):
    clusterNumber = IntegerField(
        "Cluster Number", render_kw={"placeholder": "No. of Clusters..."},
    )
    submit = SubmitField("Submit")

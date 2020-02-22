from app import app
from flask import render_template, flash, url_for, redirect
from app.forms import CheckForm, UploadDataFile
from wtforms.fields.core import BooleanField
from werkzeug.utils import secure_filename
import os
import pandas as pd
from app.statcode.datafunctions import plotCorrelation, convertCategricalToNumerical


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Liam"}
    return render_template("index.html", title="Home", user=user)


# step 1
# upload file
@app.route("/step-1-upload-file", methods=["GET", "POST"])
def uploadFile():
    form = UploadDataFile()

    if form.validate_on_submit():
        print("File upload....")
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename))

        # we wont pass df, we will just pass filename
        # df = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename))
        return redirect(url_for("catToNum", filename=filename))

    return render_template("upload.html", form=form)


# step 2
# handle categorical to numerical
@app.route("/step-2-cat-to-num/<filename>", methods=["POST", "GET"])
def catToNum(filename):
    # do data stuff
    df = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename))
    dfHead = df.head()
    colHeaders = df.columns

    # add new fields dynamically to the form class
    for val in colHeaders:
        setattr(CheckForm, val, BooleanField(val))

    form = CheckForm()

    if form.is_submitted():
        print("catToNum Submitting...")
        formData = form.data

        # use checked cols to convert to numerical
        conversionIsDone = convertCategricalToNumerical(formData, filename)

        # show correlation
        # TODO: this should be handled better(try/catch)
        if conversionIsDone:
            return redirect(
                url_for("showCorrelation", newDataFrameFileName=conversionIsDone)
            )
        else:
            flash("Working...", "message")

    # show dataframe first so they can see the numerical cols
    # show form with checkboxes beside cols
    # TODO: add css in the 'to_html method'
    return render_template(
        "cat-to-num.html",
        filename=filename,
        data=dfHead.to_html(),
        form=form,
        colHeaders=colHeaders,
    )


# step 3 Generate Correlation heatmap
@app.route("/step-3-correlation/<newDataFrameFileName>", methods=["GET"])
def showCorrelation(newDataFrameFileName):
    df = pd.read_csv(
        os.path.join(app.config["DATA_UPLOAD_FOLDER"], newDataFrameFileName)
    )
    # run plotcorrelation - this saves plot to server
    filename = plotCorrelation(df)

    return render_template("corrheatmap.html", heatMapSrc=filename)
    # can we add on a button to route to step 2?


# step 4 Drop highly correlated columns
@app.route("/step-4-drop-columns", methods=["GET", "POST"])
def form(df):
    # do data stuff
    df = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename))
    dfHead = df.head()
    colHeaders = df.columns

    # add new fields dynamically to the form class
    for val in colHeaders:
        setattr(CheckForm, val, BooleanField(val))

    form = CheckForm()

    if form.validate_on_submit():
        print("Dropping columns...")
        formData = form.data

        # function to drop columns

    return render_template(
        "dropCols.html", title="Drop Columns", form=form, colHeaders=colHeaders
    )

from app import app
from flask import render_template, flash, url_for, redirect
from app.forms import (
    CheckForm,
    UploadDataFile,
    SubsetForm,
    RedirectFormTSNE,
    RedirectFormElbow,
    ClusterNumberForm,
)
from wtforms.fields.core import BooleanField
from werkzeug.utils import secure_filename
import os
import pandas as pd
from app.statcode.datafunctions import (
    plotCorrelation,
    convertCategricalToNumerical,
    dropColumns,
    createSubsets,
    pcaVisualisation,
    elbowPlotVisualisation,
    implementKMeans,
    implementTSNE,
)


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
# TODO: make me async!
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
        # this should await
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


# step 3 Generate Correlation heatmap / choose cols to drop
@app.route("/step-3-correlation/<newDataFrameFileName>", methods=["POST", "GET"])
def showCorrelation(newDataFrameFileName):
    df = pd.read_csv(
        os.path.join(app.config["DATA_UPLOAD_FOLDER"], newDataFrameFileName)
    )
    # run plotcorrelation - this saves plot to server
    heatMapImageFileName = plotCorrelation(df)

    colHeaders = df.columns

    # add new fields dynamically to the form class
    for val in colHeaders:
        setattr(CheckForm, val, BooleanField(val))

    form = CheckForm()

    if form.is_submitted():
        print("dropping columns submitting...")
        formData = form.data

        # function to drop cols
        conversionIsDone = dropColumns(formData, newDataFrameFileName)

        return redirect(
            url_for("createSubsetsPage", newDataFrameFileName=conversionIsDone)
        )

    return render_template(
        "corrheatmap.html",
        heatMapSrc=heatMapImageFileName,
        heatMapWebPage="plotly-corrheatmap.html",
        form=form,
        colHeaders=colHeaders,
    )
    # can we add on a button to route to step 2?


# step 4 create subsets
@app.route("/step-4-subsets/<newDataFrameFileName>", methods=["POST", "GET"])
def createSubsetsPage(newDataFrameFileName):
    # do data stuff
    df = pd.read_csv(
        os.path.join(app.config["DATA_UPLOAD_FOLDER"], newDataFrameFileName)
    )
    dfHead = df.head()
    colHeaders = df.columns

    # add new fields dynamically to the form class
    for val in colHeaders:
        setattr(SubsetForm, val, BooleanField(val))

    form = SubsetForm()

    if form.is_submitted():
        print("Create Subsets Submitting...")
        formData = form.data
        subsetName = form.subsetName.data

        print("\n all form data \n", formData)
        print("\n subsetName \n", subsetName)

        # use checked cols to convert to numerical
        # this should await
        subsetFilename = createSubsets(formData, newDataFrameFileName, subsetName)

        # show correlation
        # TODO: this should be handled better(try/catch)
        if subsetFilename:
            return redirect(url_for("showPCA", subsetFilename=subsetFilename))
        else:
            flash("Working...", "message")

    # TODO: add css in the 'to_html method'
    return render_template(
        "create-subsets.html",
        filename=newDataFrameFileName,
        data=dfHead.to_html(),
        form=form,
        colHeaders=colHeaders,
    )


# Step 5 show PCA
@app.route("/step-5-pca/<subsetFilename>", methods=["POST", "GET"])
def showPCA(subsetFilename):
    pcaImgSrc = pcaVisualisation(subsetFilename)

    form = RedirectFormElbow()
    if form.is_submitted():
        return redirect(url_for("showElbowPlot", subsetFilename=subsetFilename))

    # render
    return render_template("show-pca.html", form=form, filename=pcaImgSrc)


# Step 6 Show elbow plot and form for cluster number
@app.route("/step-6-elbow-plot/<subsetFilename>", methods=["POST", "GET"])
def showElbowPlot(subsetFilename):
    elbowImageSrc = elbowPlotVisualisation(subsetFilename)
    form = ClusterNumberForm()

    if form.is_submitted():
        clusters = form.clusterNumber.data
        return redirect(
            url_for("showKMeans", clusters=clusters, subsetFilename=subsetFilename)
        )

    return render_template("elbow-plot.html", form=form, elbowImageSrc=elbowImageSrc)


# Step 7 K-Means
@app.route("/step-7-kmeans/<subsetFilename>/<clusters>", methods=["POST", "GET"])
def showKMeans(subsetFilename, clusters):
    kmeansDict = implementKMeans(subsetFilename, clusters)

    form = RedirectFormTSNE()

    if form.is_submitted():
        perplexity = form.perplexity.data
        iterations = form.iterations.data

        return redirect(
            url_for(
                "showTSNE",
                clusters=clusters,
                subsetFilename=subsetFilename,
                kmeansLabels=kmeansDict["kmeansLabels"],
                perplexity=perplexity,
                iterations=iterations,
            )
        )
    return render_template(
        "kmeans.html", form=form, kmeansImageSrc=kmeansDict["kmeansSrc"]
    )


# Step 8 TSNE
@app.route(
    "/step-8-tsne/<clusters>/<subsetFilename>/<kmeansLabels>/<perplexity>/<iterations>",
    methods=["POST", "GET"],
)
def showTSNE(clusters, subsetFilename, kmeansLabels, perplexity, iterations):

    infoDict = implementTSNE(
        subsetFilename, clusters, perplexity, iterations, kmeansLabels
    )

    subsetName = subsetFilename.split(".", 1)[0]

    return "OK"

    # return render_template(f"t-SNE-{subsetName}.html")


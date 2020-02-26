import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import plotly.graph_objs as go
import plotly.offline as offline
import plotly.figure_factory as ff
import os
from app import app
from app.statcode.helpers import zipHelper


# Importing dataset and examining it
def showDataInfo(dataset):
    print(dataset.head())
    print(dataset.shape)
    print(dataset.info())
    print(dataset.describe())


# Converting Categorical features into Numerical features
def convertCategricalToNumerical(formData, filename):
    df = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename))
    colHeaders = df.columns

    # we are going to mutate/edit the dataframe
    def myFilter(elem):
        for col in colHeaders:
            if elem[0] == col:
                return elem

    # step 1
    # Filter out un checked cols
    checkedCols = dict(filter(lambda elem: elem[1] == True, formData.items()))

    # step 2
    # Filter out non colHeaders
    finalDict = dict(filter(myFilter, checkedCols.items()))

    # step 2.5
    # list of keys
    cols = []
    for key, value in finalDict.items():
        cols.append(key)

    # step 2.9
    # create order for months
    monthsCat = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]

    # step 3
    # Iterate over each entry in that column
    # find unique entries and store in a dictionary
    uniqueColEntries = {}
    for idx, col in enumerate(cols):
        uniqueList = df[col].unique()
        # convert numpy array to list
        uniqueList = uniqueList.tolist()
        # sort modifies the list in place
        if col == "month":
            uniqueList.sort(key=lambda x: monthsCat.index(x.split()[0]))
        else:
            uniqueList.sort()
        for idx, val in enumerate(uniqueList):
            uniqueColEntries[val] = idx
        df[col] = df[col].map(uniqueColEntries)

    # write the new data frame to the server as csv and
    # we are overwriting here!
    df.to_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename), index=False)
    # the idea of this return is so that the caller knows when all the above work is done. Wanted to implement async/await but having trouble...
    return filename


# Plotting Correlation Heatmap
def plotCorrelation(dataset, filename):
    corrs = dataset.corr()
    figure = ff.create_annotated_heatmap(
        z=corrs.values,
        x=list(corrs.columns),
        y=list(corrs.index),
        annotation_text=corrs.round(2).values,
        showscale=True,
    )
    heatMapFileName = filename.split(".", 1)[0]
    filename = f"{heatMapFileName}-corrheatmap.png"
    offline.plot(
        figure,
        filename=os.path.join(
            app.config["PLOTS_UPLOAD_FOLDER"], "plotly-corrheatmap.html"
        ),
        auto_open=False,
    )
    # image quality is not great, cols are on top of each other
    figure.write_image(
        os.path.join(app.config["PLOTS_UPLOAD_FOLDER"], filename),
        width=1050,
        height=560,
        scale=1,
    )
    return filename


# Dividing dataset into label and feature sets
# drop high correlation
def dropColumns(formData, filename):
    df = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename))
    colHeaders = df.columns

    checkedCols = dict(filter(lambda elem: elem[1] == True, formData.items()))

    # we are going to mutate/edit the dataframe
    def myFilter(elem):
        for col in colHeaders:
            if elem[0] == col:
                return elem

    # Filter out non colHeaders
    finalDict = dict(filter(myFilter, checkedCols.items()))

    # list of keys
    cols = []
    for key, value in finalDict.items():
        cols.append(key)

    for col in cols:
        df.drop([col], axis=1, inplace=True)

    df.to_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename), index=False)

    return filename


def createSubsets(formData, filename, subsetName):
    df = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename))
    colHeaders = df.columns

    checkedCols = dict(filter(lambda elem: elem[1] == True, formData.items()))

    # we are going to mutate/edit the dataframe
    def myFilter(elem):
        for col in colHeaders:
            if elem[0] == col:
                return elem

    # Filter out non colHeaders
    finalDict = dict(filter(myFilter, checkedCols.items()))

    # list of keys
    cols = []
    for key, value in finalDict.items():
        cols.append(key)

    subset = df[cols]

    filename = filename.split(".", 1)[0]
    subsetNameEdited = subsetName.replace(" ", "")
    subsetFileName = f"{filename}-{subsetNameEdited}.csv"
    subset.to_csv(
        os.path.join(app.config["DATA_UPLOAD_FOLDER"], subsetFileName), index=False
    )
    return subsetFileName


### Implementing PCA to visualize dataset
def pcaVisualisation(filename):
    subset = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename))

    pca = PCA(n_components=2)

    # normaliseNumericalFeatures
    feature_scaler = StandardScaler()
    X_scaled = feature_scaler.fit_transform(subset)

    pca.fit(X_scaled)
    # print("X_scaled 2 PCA", X_scaled)
    x_pca = pca.transform(X_scaled)
    # print("X_scaled 3 PCA", X_scaled)
    # print(
    #     "Variance explained by each of the n_components: ",
    #     pca.explained_variance_ratio_,
    # )
    # print(
    #     "Total variance explained by the n_components: ",
    #     sum(pca.explained_variance_ratio_),
    # )

    plt.figure(figsize=(8, 6))
    plt.scatter(x_pca[:, 0], x_pca[:, 1], cmap="plasma")
    plt.xlabel("First Principal Component")
    plt.ylabel("Second Principal Component")
    pcaFileName = filename.split(".", 1)[0]
    filename = f"{pcaFileName}-pca.png"
    plt.savefig(os.path.join(app.config["PLOTS_UPLOAD_FOLDER"], filename))
    return filename


# Finding the number of clusters (K) - Elbow Plot Method
def elbowPlotVisualisation(subsetFilename):
    subset = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], subsetFilename))
    inertia = []
    feature_scaler = StandardScaler()
    X_scaled = feature_scaler.fit_transform(subset)
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, random_state=100)
        kmeans.fit(X_scaled)
        # kmeans.inertia_ = Sum of squared distances of samples to their closest cluster center.
        inertia.append(kmeans.inertia_)

    # print("X_scaled 5 Elbow", X_scaled)

    plt.plot(range(1, 11), inertia)
    plt.autoscale()
    plt.title("The Elbow Plot")
    plt.xlabel("Number of clusters")
    plt.ylabel("Inertia")
    elbowFileName = subsetFilename.split(".", 1)[0]
    filename = f"{elbowFileName}-elbow-plot.png"
    plt.savefig(os.path.join(app.config["PLOTS_UPLOAD_FOLDER"], filename))
    return filename


# implementing K-Means CLustering on dataset and visualizing clusters
# clusters will now be revealed through colour but will still sit on top of each other
def implementKMeans(subsetFilename, clusters):
    # get dataframe
    subset = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], subsetFilename))
    clusters = int(clusters)

    # normaliseNumericalFeatures
    feature_scaler = StandardScaler()
    X_scaled = feature_scaler.fit_transform(subset)

    # why?
    pca = PCA(n_components=2)
    pca.fit(X_scaled)

    # kmeans
    kmeans = KMeans(n_clusters=int(clusters))
    kmeans.fit(X_scaled)

    # info
    # print("X_scaled 4 kmeans", X_scaled)
    # print("Cluster Centers: \n", kmeans.cluster_centers_)

    # plot
    plt.figure(figsize=(8, 6))
    x_pca = pca.transform(X_scaled)
    plt.scatter(x_pca[:, 0], x_pca[:, 1], c=kmeans.labels_, cmap="plasma")
    plt.xlabel("First Principal Component")
    plt.ylabel("Second Principal Component")

    kmeansFileName = subsetFilename.split(".", 1)[0]
    filename = f"{kmeansFileName}-Kmeans.png"
    plt.savefig(os.path.join(app.config["PLOTS_UPLOAD_FOLDER"], filename))

    # bug passing the kmeans.labels_
    # for now we just run kmeans inside the tsne functin to get the labels
    return {"kmeansSrc": filename, "kmeansLabels": kmeans.labels_}


### Implementing t-SNE to visualize dataset
def implementTSNE(subsetFilename, clusters, perplexity, iterations):
    subset = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], subsetFilename))

    feature_scaler = StandardScaler()
    X_scaled = feature_scaler.fit_transform(subset)

    # kmeans cos we have problems passing the kmeans.labels_
    kmeans = KMeans(n_clusters=int(clusters))
    kmeans.fit(X_scaled)

    tsne = TSNE(
        n_components=int(clusters), perplexity=int(perplexity), n_iter=int(iterations)
    )
    x_tsne = tsne.fit_transform(X_scaled)

    # get cols
    colList = subset.columns

    eachColumnsValuesList = []
    for col in colList:
        eachColumnsValuesList.append(list(subset[col]))

    mergedList = [[] for i in range(len(colList))]
    for idx, colValues in enumerate(eachColumnsValuesList):
        for val in colValues:
            mergedList[idx].append(f"{colList[idx]}: " + str(val))

    hoverText = zipHelper(mergedList)

    data = [
        go.Scatter(
            x=x_tsne[:, 0],
            y=x_tsne[:, 1],
            mode="markers",
            marker=dict(color=kmeans.labels_, colorscale="Rainbow", opacity=0.5),
            text=hoverText,
            hoverinfo="text",
        )
    ]

    layout = go.Layout(
        title="t-SNE Dimensionality Reduction",
        width=700,
        height=700,
        xaxis=dict(title="First Dimension"),
        yaxis=dict(title="Second Dimension"),
    )
    fig = go.Figure(data=data, layout=layout)

    subsetName = subsetFilename.split(".", 1)[0]

    # show the interactive plot
    # subset name should be subset name not filename!
    # concat with file name for better naming!
    htmlFile = f"{subsetName}-t-SNE-.html"
    offline.plot(
        fig,
        filename=os.path.join(app.config["PLOTS_UPLOAD_FOLDER"], htmlFile),
        auto_open=True,
    )

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


# Importing dataset and examining it
# dataset = pd.read_csv("../Employees.csv")
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
    # we are overwriting shit here!
    # create new filename to smash the cache
    df.to_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename), index=False)
    # the idea of this return is so that the caller knows when all the above work is done. WAnted to implement async/await but having trouble...
    return filename


# Plotting Correlation Heatmap
def plotCorrelation(dataset):
    corrs = dataset.corr()
    figure = ff.create_annotated_heatmap(
        z=corrs.values,
        x=list(corrs.columns),
        y=list(corrs.index),
        annotation_text=corrs.round(2).values,
        showscale=True,
    )
    filename = "corrheatmap.png"
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
# drop one of the high correlation
def dropColumns(formData, filename):
    df = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename))
    colHeaders = df.columns

    checkedCols = dict(filter(lambda elem: elem[1] == True, formData.items()))
    print("\n\n checked incl submit etc...\n", checkedCols)
    # we are going to mutate/edit the dataframe
    def myFilter(elem):
        for col in colHeaders:
            if elem[0] == col:
                return elem

    # Filter out non colHeaders
    finalDict = dict(filter(myFilter, checkedCols.items()))
    print("\n\n removed submit etc...\n", finalDict)

    # list of keys
    cols = []
    for key, value in finalDict.items():
        cols.append(key)
    print("\n\n just the checked col headers...\n", cols)

    for col in cols:
        print("\n gonna drop the ", col, "column")
        df.drop([col], axis=1, inplace=True)

    print("\n Current list of cols: ", df.columns)

    df.to_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename), index=False)

    return filename

    # return dataset.drop(["poutcome"], axis=1)  # Features


#### need to run the elbow plot on every subset to find the number of clusters ###


def createSubsets(formData, filename, subsetName):
    df = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename))
    colHeaders = df.columns

    checkedCols = dict(filter(lambda elem: elem[1] == True, formData.items()))
    print("\n\n checked incl submit etc...\n", checkedCols)
    # we are going to mutate/edit the dataframe
    def myFilter(elem):
        for col in colHeaders:
            if elem[0] == col:
                return elem

    # Filter out non colHeaders
    finalDict = dict(filter(myFilter, checkedCols.items()))
    print("\n\n removed submit etc...\n", finalDict)

    # list of keys
    cols = []
    for key, value in finalDict.items():
        cols.append(key)
    print("\n\n just the checked col headers...\n", cols)

    subset = df[cols]
    # write the new subset, dynamic name pls!
    filename = subsetName.replace(" ", "")
    filename = filename + ".csv"  # needed?
    subset.to_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], filename), index=False)
    return filename


### Implementing PCA to visualize dataset
# we see that all the points are on top of each other so we decide to use t-SNE instead
# That is all we are doing here, looking at PCA, deciding, nah, and moving onto t-SNE
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
    filename = "pca.png"
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
    plt.title("The Elbow Plot")
    plt.xlabel("Number of clusters")
    plt.ylabel("Inertia")
    filename = "elbow-plot.png"
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
    kmeans = KMeans(n_clusters=clusters)
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

    filename = "Kmeans.png"
    plt.savefig(os.path.join(app.config["PLOTS_UPLOAD_FOLDER"], filename))

    return {"kmeansSrc": filename, "kmeansLabels": kmeans.labels_}


### Implementing t-SNE to visualize dataset
def implementTSNE(subsetFilename, clusters, perplexity, iterations, kmeansLabels):
    subset = pd.read_csv(os.path.join(app.config["DATA_UPLOAD_FOLDER"], subsetFilename))
    # feature_scaler = StandardScaler()
    # X_scaled = feature_scaler.fit_transform(subset)

    # tsne = TSNE(
    #     n_components=int(clusters), perplexity=int(perplexity), n_iter=int(iterations)
    # )
    # x_tsne = tsne.fit_transform(X_scaled)

    # print("X_scaled 6 t-SNE", X_scaled)

    # get cols
    colList = subset.columns
    print(f"\n colList: ${colList}")

    # bigList = []
    # for col in colList:
    #     bigList.append(list(subset[col]))

    listOfColumnValues = list(subset[colList[0]])
    print(f"\n listOfColumnValues: {listOfColumnValues[0:10]}")

    # text = [f"Age: {a};" for a in list(zip(listOfColumnValues[0:10]))]
    # print(f"\n Text: {text}")

    return {"colList": colList, "listOfColumnValues": listOfColumnValues}
    # replace with subset
    # Age = list(subset["Age"])
    # Gender = list(subset["Gender"])
    # Education = list(subset["Education"])
    # EducationField = list(subset["EducationField"])
    # DistanceFromHome = list(subset["DistanceFromHome"])
    # MaritalStatus = list(subset["MaritalStatus"])

    # data = [
    #     go.Scatter(
    #         x=x_tsne[:, 0],
    #         y=x_tsne[:, 1],
    #         mode="markers",
    #         marker=dict(color=kmeansLabels, colorscale="Rainbow", opacity=0.5),
    #         # replace with subset
    #         text=[
    #             f"Age: {a}; Gender: {b}; Education:{c}; EducationField:{d}; DistanceFromHome:{e}; MaritalStatus:{f}"
    #             for a, b, c, d, e, f in list(
    #                 zip(
    #                     Age,
    #                     Gender,
    #                     Education,
    #                     EducationField,
    #                     DistanceFromHome,
    #                     MaritalStatus,
    #                 )
    #             )
    #         ],
    #         hoverinfo="text",
    #     )
    # ]

    # layout = go.Layout(
    #     title="t-SNE Dimensionality Reduction",
    #     width=700,
    #     height=700,
    #     xaxis=dict(title="First Dimension"),
    #     yaxis=dict(title="Second Dimension"),
    # )
    # fig = go.Figure(data=data, layout=layout)

    # # save the file
    # subsetName = subsetFilename.split(".", 1)[0]
    # filename = f"t-SNE-{subsetName}.png"
    # plt.savefig(os.path.join(app.config["PLOTS_UPLOAD_FOLDER"], filename))
    # # show the interactive plot
    # htmlFile = f"t-SNE-{subsetName}.html"
    # offline.plot(
    #     fig,
    #     filename=os.path.join(app.config["PLOTS_UPLOAD_FOLDER"], filename=htmlFile),
    #     auto_open=False,
    # )


# need to run the elbow plot on every subset to find the number of clusters
# where do we use the number of clusters that we get from the elbow plot


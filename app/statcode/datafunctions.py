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
    # return filename
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
    # offline.plot(figure, filename="corrheatmap.html")
    # image quality is not great, cols are on top of each other
    figure.write_image(os.path.join(app.config["PLOTS_UPLOAD_FOLDER"], filename))
    return filename


# Dividing dataset into label and feature sets
# drop one of the high correlation
def dropFeatures(dataset):
    return dataset.drop(["poutcome"], axis=1)  # Features


# create subsets because even though we dropped some cols, we still have too many
# try this with - age, gender, marital status, education, educationField,

#### need to run the elbow plot on every subset to find the number of clusters ###


def createSubsets(dataset):
    subsetChurn = dataset[
        [
            "Age",
            "Gender",
            "MaritalStatus",
            "Education",
            "EducationField",
            "DistanceFromHome",
        ]
    ]  # specify cols or...
    # subset2 = dataset.iloc[:,0:8] # specify cols by index

    # maybe assign the return of createSubsets to X instaed


# X = subsetChurn

## Normalizing numerical features so that each feature has mean 0 and variance 1
def normaliseNumericalFeatures(subset):
    feature_scaler = StandardScaler()
    X_scaled = feature_scaler.fit_transform(subset)
    print("X_scaled 1", X_scaled)


### Implementing PCA to visualize dataset
# we see that all the points are on top of each other so we decide to use t-SNE instead
# That is all we are doing here, looking at PCA, deciding, nah, and moving onto t-SNE
def pcaVisualisation(subset1):
    pca = PCA(n_components=2)
    feature_scaler = StandardScaler()
    X_scaled = feature_scaler.fit_transform(subset1)
    pca.fit(X_scaled)
    print("X_scaled 2 PCA", X_scaled)
    x_pca = pca.transform(X_scaled)
    print("X_scaled 3 PCA", X_scaled)
    print(
        "Variance explained by each of the n_components: ",
        pca.explained_variance_ratio_,
    )
    print(
        "Total variance explained by the n_components: ",
        sum(pca.explained_variance_ratio_),
    )

    plt.figure(figsize=(8, 6))
    plt.scatter(x_pca[:, 0], x_pca[:, 1], cmap="plasma")
    plt.xlabel("First Principal Component")
    plt.ylabel("Second Principal Component")
    plt.savefig("PCA.png")
    # plt.show()


# implementing K-Means CLustering on dataset and visualizing clusters
def implementKMeans(subset):
    feature_scaler = StandardScaler()
    pca = PCA(n_components=2)
    kmeans = KMeans(n_clusters=2)  # elbow is at 2 so we should only have 2 clusters
    X_scaled = feature_scaler.fit_transform(subset)
    kmeans.fit(X_scaled)
    print("X_scaled 4 kmeans", X_scaled)
    print("Cluster Centers: \n", kmeans.cluster_centers_)
    plt.figure(figsize=(8, 6))
    x_pca = pca.transform(X_scaled)
    plt.scatter(x_pca[:, 0], x_pca[:, 1], c=kmeans.labels_, cmap="plasma")
    plt.xlabel("First Principal Component")
    plt.ylabel("Second Principal Component")
    plt.savefig("KMeans.png")


# Finding the number of clusters (K) - Elbow Plot Method
def elbowPlotVisualisation(subset):
    inertia = []
    feature_scaler = StandardScaler()
    X_scaled = feature_scaler.fit_transform(subset)
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, random_state=100)
        kmeans.fit(X_scaled)
        # kmeans.inertia_ = Sum of squared distances of samples to their closest cluster center.
        inertia.append(kmeans.inertia_)

    print("X_scaled 5 Elbow", X_scaled)

    plt.plot(range(1, 11), inertia)
    plt.title("The Elbow Plot")
    plt.xlabel("Number of clusters")
    plt.ylabel("Inertia")
    plt.savefig("Elbow.png")


### Implementing t-SNE to visualize dataset
def implementTSNE(subset):
    feature_scaler = StandardScaler()
    X_scaled = feature_scaler.fit_transform(subset)
    tsne = TSNE(n_components=2, perplexity=50, n_iter=3000)
    x_tsne = tsne.fit_transform(X_scaled)
    print("X_scaled 6 t-SNE", X_scaled)

    Age = list(subset["Age"])
    Gender = list(subset["Gender"])
    Education = list(subset["Education"])
    EducationField = list(subset["EducationField"])
    DistanceFromHome = list(subset["DistanceFromHome"])
    MaritalStatus = list(subset["MaritalStatus"])

    data = [
        go.Scatter(
            x=x_tsne[:, 0],
            y=x_tsne[:, 1],
            mode="markers",
            marker=dict(color="#F00", colorscale="Rainbow", opacity=0.5),
            text=[
                f"Age: {a}; Gender: {b}; Education:{c}; EducationField:{d}; DistanceFromHome:{e}; MaritalStatus:{f}"
                for a, b, c, d, e, f in list(
                    zip(
                        Age,
                        Gender,
                        Education,
                        EducationField,
                        DistanceFromHome,
                        MaritalStatus,
                    )
                )
            ],
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
    offline.plot(fig, filename="t-SNE.html")


# need to run the elbow plot on every subset to find the number of clusters
# where do we use the number of clusters that we get from the elbow plot


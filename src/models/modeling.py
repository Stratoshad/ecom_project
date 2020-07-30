"""
MODELING Module
---------------

@author : Stratoshad

This module contains various functions
that relate to the differnt modeling
techniques applied in this project.

"""

import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict
from tqdm import tqdm
import pandas as pd
import plotly.express as px


def log_scale_dataset(df):

    """
    Takes in a dataframe of
    numerical columns and 
    transforms it using the
    np.logp1 function.
    
    Parameters:
    -----------
    
    df : dataframe
    
    Dataframe with numerical 
    values to be scaled
    
    Returns:
    --------
    
    df_out : dataframe
    
    Dataframe with scaled values
    
    """

    df_scaled = df.copy()
    all_cols = df_scaled.columns

    # We use np.logp1 instead of log
    # as it copes deals a lot better
    # with very small values
    # https://numpy.org/doc/stable/reference/generated/numpy.log1p.html
    for col in all_cols:
        df_scaled[col] = np.log1p(df_scaled[col])

    return df_scaled


def run_kmeans(df, cluster_num, fit_only=False, iter_num=1000):

    """
    Runs a kmeans algorithm using
    the sklearn library. 
    
    Paramaters:
    -----------
    
    df : dataframe
    
    Dataframe to cluster
    
    cluster_num : int
    
    The number of clusters to use
    for the algorithm
    
    fit_only : bool (default = False)
    
    If True it only fits the model
    and returns the model rather than
    getting the results. If False it 
    returns both the clusters and the
    model class.
    
    iter_num : int
    
    The number of iterations to run
    the model for.
    
    Returns:
    --------
    
    model : sklearn class
    
    The model class with all 
    its artifacts
    
    results : numpy array
    
    An array of all cluster labels
    predicted by the model. Only if
    fit_only is False
    
    """

    values = df.copy()

    # Define the model we use kmeans++
    # as the initialisation which used
    # "smart" initializing
    # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html

    model = KMeans(n_clusters=cluster_num, init="k-means++", max_iter=iter_num)

    # If we want to only return the
    # model then we use the fit only
    # method. This is useful when you
    # are running the "Elbow Method"
    if fit_only:
        model.fit(values)
        return model

    else:
        results = model.fit_predict(values)
        return model, results


def create_elbow_fig(df):

    """
    Takes in a dataframe
    of inertia and cluster
    number and plots the
    elbow method.
    
    Parameters:
    -----------
    
    df : dataframe
    
    Dataframe with inertia 
    values and cluster numbers
    
    Returns:
    --------
    
    fig : plotly figure
    
    The elbow method figure
    
    """

    # Copy the dataframe and build a line chart to
    # represent the elbow method
    df_elbow = df.copy()

    fig = px.line(
        df_elbow,
        x="cluster_num",
        y="intertia",
        title="Elbow Method Chart Inertia vs Number of Clusters",
        template="ggplot2",
    )

    fig.update_traces(line_width=3)

    fig.update_layout(title_font_size=14, font_size=10)

    fig.update_yaxes(title="Intertia")
    fig.update_xaxes(title="Number of Clusters", dtick=1)

    return fig


def run_elbow_method(df, max_clusters, iter_num=1000):

    """
    Takes in a dataframe and 
    runs the elbow method 
    for a max number of iterations.
    It then plots the elbow 
    chart.
    
    Parameters:
    -----------
    
    df : dataframe
    
    The dataframe to cluster
    
    max_clusters : int
    
    The maximum number of clusters
    to test for.
    
    iter_num : int
    
    The number of iterations to run
    the model for.
    
    Returns:
    --------
    
    df_elboew : dataframe
    
    The dataframe with the inertia
    scores and the number of
    clusters
    
    fig : plotly figure
    
    The elbow method figure
    
    """

    # Initialize all variables
    score_dict = defaultdict(list)

    # For each cluster create a model
    # and get the inerti value, then
    # add the inertia and the cluster
    # number to the dictionary
    for cluster in tqdm(range(1, max_clusters + 1)):

        model = run_kmeans(df=df, cluster_num=cluster, fit_only=True, iter_num=iter_num)

        inertia = model.inertia_
        score_dict["cluster_num"].append(cluster)
        score_dict["intertia"].append(inertia)

    # Create a dataframe and visualise it
    df_elbow = pd.DataFrame(score_dict)
    fig = create_elbow_fig(df=df_elbow)

    return fig, df_elbow

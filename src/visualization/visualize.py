"""
VISUALIZE Module
----------------

@author : Stratoshad

This module contains various
Python functions that produce
charts and visuals. Most of them
return the figure.

"""

import plotly.express as px
from src.data import utils


def make_histogram(
    df, col_name, hist_color, color_by=None, cap=False, q_cap=0.95, marginal="box"
):

    """
    Takes in a dataframe and a column
    name and creates a simple histogram
    using the plotly library. It also 
    creates a "boxplot" by default on top.
    
    Parameters:
    -----------
    
    df : dataframe
    
    The dataframe to plot
    
    col_name : string 
    
    The column name to plot the 
    distribution of
    
    color : str
    
    The color of the histogram. Takes in
    all standard color types (hex, rgb etc.)
    
    cap_col : boolean (default = False)
    
    Whether to cap the column
    using a given percentile
    
    q_cap : float (default = 0.95)
    
    The percentile to use to cap the
    column
    
    marginal : str (default = "box")
    
    The marginal to have on top. If None
    provided it doesn't plot any. Takes
    standard inputs of px.histogram()
    
    Returns:
    
    fig : plotly figure
    
    The plotted histogram
    
    """

    df_plot = df.copy()

    # Check whether the column requires
    # cap. If yes then cap it using the
    # given percentile
    if cap:
        df_plot[col_name] = utils.cap_col(df[col_name], q=q_cap)

    fig = px.histogram(
        df_plot,
        x=col_name,
        color=color_by,
        title=f"Distribution of {col_name}",
        template="ggplot2",
        marginal=marginal,
    )

    # We define a standard layout to allow for consistent
    # graphs
    fig.update_traces(
        marker_color=hist_color,
        marker_line_color="rgb(45, 46, 45)",
        marker_line_width=1.5,
        opacity=0.9,
    )

    return fig

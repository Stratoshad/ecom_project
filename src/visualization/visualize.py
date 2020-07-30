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
    df,
    col_name,
    color,
    title=None,
    hover_cols=None,
    cap=False,
    q_cap=0.95,
    marginal="box",
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

    title : str (default = None)

    The title at the top of the chart

    hover_cols : list (default = None)

    A list of columns from the dataframe to
    appear on hovering the chart
    
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

    if title is None:
        title = f"Distribution of {col_name}"

    # Check whether the column requires
    # cap. If yes then cap it using the
    # given percentile
    if cap:
        df_plot[col_name] = utils.cap_col(df[col_name], q=q_cap)

    if color in df_plot.columns:

        fig = px.histogram(
            df_plot,
            x=col_name,
            color=color,
            hover_data=hover_cols,
            title=title,
            template="ggplot2",
            marginal=marginal,
        )

    else:

        fig = px.histogram(
            df_plot,
            x=col_name,
            hover_data=hover_cols,
            title=title,
            template="ggplot2",
            marginal=marginal,
        )

        fig.update_traces(marker_color=color)

    # We define a standard layout to allow for consistent
    # graphs
    fig.update_traces(
        marker_line_color="rgb(45, 46, 45)", marker_line_width=1.5, opacity=0.9,
    )

    fig.update_layout(title_font_size=14, font_size=10)

    return fig


def make_barchar(df, x_axis, y_axis, color, text_col=None, title=None):

    """
    Takes in a dataframe and a column
    name and creates a simple barchart
    using the plotly library. It also 
    creates a "boxplot" by default on top.
    
    Parameters:
    -----------
    
    df : dataframe
    
    The dataframe to plot
    
    x_axis : str
    
    The column shown on the x-axis
    of the chart
    
    y_axis : str
    
    The column shown o nthe y-axis
    of the chart
    
    color : str
    
    The color of the histogram. Takes in
    all standard color types (hex, rgb etc.)
    
    text_col : str (default = None)
    
    The column to show on at the top
    of the bars
    
    Returns:
    
    fig : plotly figure
    
    The plotted histogram
    
    """

    df_plot = df.copy()

    # Check whether a title was passed
    # if not just create a generic title
    if title is None:
        title = f"Bar chart of {y_axis} vs {x_axis}"

    fig = px.bar(
        df_plot, x=x_axis, y=y_axis, title=title, text=text_col, template="ggplot2",
    )

    # We define a standard layout to allow for consistent
    # graphs
    fig.update_traces(
        textposition="outside",
        marker_color=color,
        marker_line_color="rgb(45, 46, 45)",
        marker_line_width=1,
        opacity=0.9,
    )

    fig.update_xaxes(title_font_size=12, tickfont_size=11)
    fig.update_yaxes(title_font_size=12, tickfont_size=11)

    return fig


def make_scatter(
    df, x_axis, y_axis, title, color_by, x_axis_title=None, y_axis_title=None
):

    """
    Creates a scatter plot using the
    Ploty graphing library
    
    Parameters:
    
    df : dataframe
    
    The dataframe to plot from
    
    x_axis : str
    
    The name of the x axis column
    
    y_axis : str
    
    The name of the y axis columns
    
    color_by : str
    
    The column to color by
    
    x_axis_title : str (default = None)
    
    The axis title to display
    
    y_axis_title : str (default = None)
    
    The y_axis title
    
    Returns:
    --------
    
    fig : plotly_figure
    
    The scatter plot figure
    
    """

    df_plot = df.copy()

    if x_axis_title is None:
        x_axis_title = x_axis

    if y_axis_title is None:
        y_axis_title = y_axis

    if color_by not in df_plot.columns:

        # Create the scatter plot figure
        fig = px.scatter(df_plot, x=x_axis, y=y_axis, title=title, template="ggplot2")

        fig.update_traces(marker_color=color_by)
    else:

        # Create the scatter plot figure
        fig = px.scatter(
            df_plot, x=x_axis, y=y_axis, color=color_by, title=title, template="ggplot2"
        )

    # Update the layout and the traces
    # to keep a consistent look
    fig.update_traces(marker_size=7, marker_line_width=0.5)

    fig.update_layout(
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        height=650,
        title_font_size=14,
        font_size=10,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            title=None,
            font_size=11,
            xanchor="right",
            x=0.76,
        ),
    )

    return fig

"""
UTILS Module
------------

@author : Stratoshad

This module contains generic python
functionality that automates common
tasks you do during a project.
"""

import pandas as pd


def print_bold(txt):
    """
    Function that prints
    input text as bold using
    the print() function.

    Parameters:
    -----------

    txt : string

    Text to print in bold

    Returns:
    --------

    None

    """

    print("\033[1m" + txt + "\033[0m")

    return


def quick_summary(df, title, row_num=5, show_summary=True):
    """
    Returns a quick summary
    of a given dataset

    Parameters:
    -----------

    df : dataframe

    The dataframe to return
    the summary

    title : string

    The title of the dataframe

    row_num : int (default = 5)

    The number of rows to return
    of the dataframe

    show_summary : bool (default = True)

    Print the summary of dtypes and 
    null values as well as a preview

    Return:
    -------

    None

    """

    # Print the title
    print("\n")
    print_bold(f"{title.upper()}")
    print("-" * (len(title) + 1))
    print("\n")
    print(f"Number of rows: {df.shape[0]} \t Number of Columns: {df.shape[1]}")

    # Print the dataframe
    display(df.head(row_num))

    if show_summary:
        # Get the overall summary
        print("\n\n")
        print_bold("OVERALL SUMMARY")
        print("-" * 15)
        print(df.info())

    return


def missing_summary(df):
    """
    Takes in a dataframe and 
    returns a summary of all
    missing values.
    
    Parameters:
    -----------
    
    df : dataframe
    
    Dataframe to calculate the
    missing summary from.
    
    Returns:
    --------
    
    df_miss : dataframe
    
    Missing values summary
    
    """

    # Copy for output
    df_out = df.copy()

    # Create a new summary dataframe
    # for each column.
    df_miss = df_out.notnull().sum().reset_index()
    df_miss["Missing"] = df_out.isnull().sum().values
    df_miss["Percentage Missing"] = (
        (df_miss["Missing"] / df_out.shape[0]) * 100
    ).round(1)

    # Rename all the columns
    df_miss.columns = ["Column", "Not-Null", "Missing", "Perc Missing (%)"]

    return df_miss

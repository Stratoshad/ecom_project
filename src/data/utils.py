"""
UTILS Module
------------

@author : Stratoshad

This module contains generic python
functionality that automates common
tasks you do during a project.
"""

import pandas as pd


def rearrange_and_rename(df, col_order, rename_dict=None):
    """
    Takes in a dataframe, a column
    order and optionally a rename
    dictionary. It rearranges the 
    column order by putting the ones
    defined in "col_order" first. It
    retains the order of the remaining 
    ones.
    
    Parameters:
    -----------
    
    df : dataframe
    
    Dataframe to rearrange
    
    col_order : list
    
    List of the columns to go at
    the beginning of the dataframe
    
    rename_dict : dictionary
    
    Dictionary
    """

    df_out = df.copy()

    # Rearrange the columns based on
    # the order provided
    other_cols = [col for col in df_out.columns if col not in col_order]
    df_out = df_out[col_order + other_cols]

    if rename_dict is not None:
        # Rename using the rename dictionary
        df_out = df_out.rename(columns=rename_dict)

    return df_out


def cap_col(col, q):
    """
    Takes in a column
    and caps it at the 
    given quantile
    
    Parameters:
    -----------
    
    col : series
    
    A pandas series column
    to cap
    
    q : float (ranging 0-1)
    
    The quantile to cap at
    
    Returns
    -------
    
    col_capped : series
    
    The column with the capped values
    
    """

    cap_val = col.quantile(q)

    return col.apply(lambda x: cap_val if x > cap_val else x)


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

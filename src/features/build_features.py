"""
BUILD_FEATURES Module
---------------------

@author : Stratoshad

This module contains function
that relate to data pre-processing
or aggregation.

"""

from tqdm import tqdm
import pandas as pd
import numpy as np
from datetime import datetime
import warnings


def process_cancellations(df, limit_rows=None):
    """
    Takes in the dataframe of transactions
    and identifies all cancellations. It
    then runs through the following logic
    to identify matches for those cancellations.
    
    For each cancellation identifies all transactions
    that have the same CustomerID, StockCode are in
    the past and have the same or less Quantity. It excludes 
    cancellations with no CustomerID.
    
    For cancellations with no matches it just takes
    a note of the index. For single matches it adds
    the canceled quantity to the original dataframe.
    For multi-matches it either picks up the transaction
    with an exact match on Quantity or keeps eliminating
    transactions until it covers all cancellation 
    quantities.
    
    Parameters:
    -----------
    
    df : dataframe
    
    A dataframe of transactions that
    has the "Cancelled" column
    
    limit_rows : int (default : None)
    
    Limits the numbers of cancellations to
    look through. This is useful for testing. If
    None looks through all of them.
    
    Returns:
    --------
    
    df_clean : dataframe
    
    A dataframe with all canceled transactions
    dropped and the paired ones marked down.
    
    match_dict : dictionary
    
    A dictionary of all indices of the 
    cancellation transactions split by their
    matched category
    
    """

    # Create the main dataframes
    df_clean = df.copy()
    df_cancel = df_clean.loc[
        (df_clean["Cancelled"] == 1) & (df_clean["CustomerID"] != "00000")
    ]
    incomplete_cancelations = []

    # Intilize the dictionary and the columns
    match_dict = {"no_match": [], "one_match": [], "mult_match": []}
    df_clean["Quantity_Canc"] = 0
    df_clean["Cancel_Date"] = np.nan

    if limit_rows is not None:

        df_cancel = df_cancel.iloc[:limit_rows]

    for index, row in tqdm(df_cancel.iterrows(), total=df_cancel.shape[0]):
        #     for index, row in df_cancel.iterrows():
        # Extract all useful information
        customer_id = row["CustomerID"]
        stock_code = row["StockCode"]
        canc_quantity = row["Quantity"]
        canc_date = row["InvoiceDate"]

        # Get all transactions that have the
        # same customerID and Stock Code but
        # happened earlier than the cancellation
        df_tmp = df_clean.loc[
            (df_clean["CustomerID"] == customer_id)
            & (df_clean["StockCode"] == stock_code)
            & (df_clean["InvoiceDate"] <= canc_date)
            & (df_clean["Cancelled"] != 1)
        ]

        # If we have no matches just record
        # that cancelation as unmatches
        if df_tmp.shape[0] == 0:

            match_dict["no_match"].append(index)

        # If we have only one match then take that
        # as its match. Ensure we get the minimum between
        # the quantity match and the available cancelations
        elif df_tmp.shape[0] == 1:

            matched = df_tmp.iloc[0]
            quantity_bought = matched["Quantity"]
            already_canc = matched["Quantity_Canc"]

            # If we don't find enough purchases to match
            # the cancelations then keep track of them
            if quantity_bought < (canc_quantity * -1):

                incomplete_cancelations.append(index)

            if (quantity_bought - already_canc) >= (canc_quantity * -1):

                match_dict["one_match"].append(index)

                # Take the minimum between remainder and total bought
                actual_cancel = min(quantity_bought, (canc_quantity * -1))

                # Update the original dataframe
                df_clean.loc[matched.name, "Quantity_Canc"] += actual_cancel
                df_clean.loc[matched.name, "Cancel_Date"] = canc_date

            #                 print()
            #                 print(index)
            #                 display(df_cancel.loc[index:index, :])
            #                 display(df_tmp)
            #                 print()

            #                 print(f"{matched.name} was chosen with {actual_cancel} taken out of it.")
            #                 display(df_clean.loc[matched.name:matched.name, :])
            #                 print()

            else:
                match_dict["no_match"].append(index)

        # In the case that we have more than one matches the follow
        # rules apply. If there is an exact match to the quantity take the
        # most recent one. Otherwise keep taking recent transactions until
        # you get all total cancelations.
        elif df_tmp.shape[0] > 1:

            match_dict["mult_match"].append(index)

            #             print()
            #             print(index)
            #             display(df_cancel.loc[index:index, :])
            #             display(df_tmp)
            #             print()

            # Check if there are any exact matches or greater matches of Quantity
            exact_matches = df_tmp.loc[
                (df_tmp["Quantity"] == (canc_quantity * -1))
                & (
                    df_tmp["Quantity"]
                    >= (df_tmp["Quantity_Canc"] + (canc_quantity * -1))
                )
            ]

            if len(exact_matches) == 0:

                # Loop through the array from bottom up
                # and only mark transactions until you
                # match the total quantity canceled
                cum_quant = 0

                for idx, r in df_tmp[::-1].iterrows():

                    quantity_bought = r["Quantity"] - r["Quantity_Canc"]
                    quantity_left = quantity_bought - r["Quantity_Canc"]

                    if quantity_left <= (canc_quantity * -1):

                        continue

                    elif cum_quant < (canc_quantity * -1):

                        # Ensure we are only assigning as much
                        # quantity as available
                        remainder = (canc_quantity * -1) - cum_quant
                        actual_cancel = min(quantity_bought, remainder)
                        cum_quant += actual_cancel
                        #                         print(f"Cancelled {actual_cancel} / {quantity_bought} of order {idx}")
                        #                         print(f"Added transaction {idx} and cum_quant is now: {cum_quant} / {canc_quantity * -1}")

                        # Update the original dataframe
                        df_clean.loc[idx, "Quantity_Canc"] += actual_cancel
                        df_clean.loc[idx, "Cancel_Date"] = canc_date

            # Take the latest exact match as
            # the correct transaction
            else:

                matched = exact_matches.iloc[-1]

                idx = matched.name
                actual_cancel = canc_quantity * -1

                # Update the original dataframe
                df_clean.loc[idx, "Quantity_Canc"] += actual_cancel
                df_clean.loc[idx, "Cancel_Date"] = canc_date

    #                 print(f"{idx} was chosen.")
    #                 display(df_clean.loc[idx:idx, :])
    #                 print()

    # Print the summary
    print(f"Total Cancelation Summary")
    print(f"Total Cancelations: {df_cancel.shape[0]}")
    print(
        f"No-Matches: {len(match_dict['no_match'])} ({round((len(match_dict['no_match']) / df_cancel.shape[0] * 100), 1)}%)"
    )
    print(
        f"Single-Matches: {len(match_dict['one_match'])} ({round((len(match_dict['one_match']) / df_cancel.shape[0] * 100), 1)}%)"
    )
    print(
        f"Multi-Matches: {len(match_dict['mult_match'])} ({round((len(match_dict['mult_match']) / df_cancel.shape[0] * 100), 1)}%)"
    )

    # At the end ensure that we don't have any canceled quantities above
    # the actual quantity except for Discounts
    df_test = df_clean[
        (df_clean["Cancelled"] != 1) & (df_clean["StockCode"] != "D")
    ].copy()
    assert (
        df_test["Quantity"] < df_test["Quantity_Canc"]
    ).sum() == 0, "There are transactions with canceled quantities > bought quantities"

    return df_clean, match_dict


def get_df_date_features(date_df, date_column):

    """
    Takes in a dataframe and the corresponding
    date_column. From that it extracts the following
    information:

    - Month
    - Month Name
    - Day
    - Week Num
    - Season
    - Year
    - Is_Weekend

    Parameters
    ----------

    date_df: dataframe

    A timeseries dataset that contains
    a date column where features can be
    extracted from.

    date_column: str

    Column name of where the dates
    are in the dataframe

    Returns
    -------

    edited_df: dateframe

    Dataframe with the features mentioned
    above added as columns

    """

    # Copy the dataframe
    df_edited = date_df.copy()

    df_edited[date_column] = pd.to_datetime(df_edited[date_column])

    # Get the Year / Date / Month / Day / Week
    dates = list(df_edited[date_column].dt.strftime("%d/%m/%Y"))
    years = list(df_edited[date_column].dt.year)
    months = list(df_edited[date_column].dt.month)
    month_names = list(df_edited[date_column].dt.month_name().apply(lambda x: x[:3]))
    days = list(df_edited[date_column].dt.day_name().apply(lambda x: x[:3]))
    day_num = list(df_edited[date_column].dt.day)
    weeks = list(df_edited[date_column].dt.week)

    # Add the seasons
    d = {
        "Winter": [12, 1, 2],
        "Spring": [3, 4, 5],
        "Summer": [6, 7, 8],
        "Autumn": [9, 10, 11],
    }
    seasons = []

    # Go through all months and find out which season they belong
    for x in months:

        for key, value in d.items():

            if x in value:
                seasons.append(key)

                continue

            continue

    # Add to dataset
    df_edited["month"] = month_names
    df_edited["day"] = days
    df_edited["day_num"] = day_num
    df_edited["date"] = dates
    df_edited["date"] = pd.to_datetime(df_edited["date"], format="%d/%m/%Y")
    df_edited["week_in_year"] = weeks
    df_edited["year"] = years
    df_edited["season"] = seasons

    # Create the christmas_hol columns
    df_edited["is_christmas"] = (
        (df_edited["week_in_year"] >= 49) | (df_edited["week_in_year"] <= 2)
    ).astype(int)

    # Create the is_weekend column
    df_edited["is_weekend"] = (
        (df_edited["day"] == "Sun") | (df_edited["day"] == "Sat")
    ).astype(int)

    # Create the year + month col
    df_edited["month_n_year"] = df_edited["month"] + " " + df_edited["year"].astype(str)

    return df_edited


def get_customer_lifetime(df_cust, ref_date, start_date):
    """
    Takes in a customer dataframe and
    returns the customer lifetime based
    on a reference date.
    
    Parameters:
    -----------
    
    df_cust : dataframe
    
    Customer dataframe
    
    ref_date : str
    
    Reference date to calculate the
    lifetime from
    
    start_date : str
    
    The starting reference day
    
    Returns:
    --------
    
    df_life : dataframe
    
    Dataframe of customers including
    the lifetime
    
    """

    df_life = df_cust.copy()

    # Convert date to datetime
    ref_date = datetime.strptime(ref_date, "%Y-%m-%d %H:%M:%S")
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    diff = (ref_date - start_date).days

    # Find the difference in days
    df_life["first_purchase"] = pd.to_datetime(
        df_life["first_purchase"], format="%Y-%m-%d %H:%M:%S"
    )
    df_life["lifetime"] = (ref_date - df_life["first_purchase"]).astype(
        "timedelta64[s]"
    )
    df_life["lifetime"] = (df_life["lifetime"] / (24 * 3600)).round(1)
    df_life["period_perc"] = (df_life["lifetime"] / diff).round(3)

    return df_life


def get_purchase_freq(df_inv, df_cust):

    """
    Takes in a dataframe of invoices
    and a dataframe of customers and
    finds the time between invoices
    for each customer. It then aggregates
    them.
    
    Parameters:
    -----------
    
    df_inv : dataframe
    
    Dataframe with all invoices
    
    df_cust : dataframe
    
    Dataframe with all customers
    
    Returns:
    --------
    
    df_freq : dataframe
    
    Dataframe aggregated at the
    customer level with the frequency
    metric
    
    """

    # Copy the dataframes
    df_cust_ind = df_cust.copy()
    df_main = df_inv.copy()

    # Get all the relevant customer ids
    # and loop through each of them
    unq_ids = df_cust_ind.customer_id.unique()
    rel_cols = ["customer_id", "invc_num", "invc_date"]
    df_list = []

    for cust_id in tqdm(unq_ids):

        # Filter the invoice dataset for that ID
        # and extract the relevant columns
        df_filt = df_main.loc[df_main["customer_id"] == cust_id, rel_cols].copy()
        df_filt = df_filt.sort_values(by="invc_date", ascending=True)

        # Get the date of the last invoice and find the
        # difference in days
        df_filt["last_date"] = df_filt["invc_date"].shift(1)
        df_filt["last_date"] = pd.to_datetime(
            df_filt["last_date"], format="%Y-%m-%d %H:%M:%S"
        )
        df_filt["invc_date"] = pd.to_datetime(
            df_filt["invc_date"], format="%Y-%m-%d %H:%M:%S"
        )
        df_filt["invc_delta"] = (df_filt["invc_date"] - df_filt["last_date"]).astype(
            "timedelta64[s]"
        )
        df_filt["invc_delta"] = (df_filt["invc_delta"] / (24 * 3600)).round(3)
        df_filt = df_filt.drop("last_date", axis=1).dropna()

        # Add the dataframe into the list to be combined
        # with the others later on
        df_list.append(df_filt)

    # Combine all the dataframes and combine
    # with the customer dataframe
    df_freq = pd.concat(df_list).reset_index(drop=True)
    df_freq = df_freq.groupby("customer_id").agg(
        {"invc_delta": ["min", "median", "mean", "max", "std"]}
    )
    df_freq.columns = df_freq.columns.droplevel(0)
    df_freq = df_freq.reset_index()
    df_freq = df_cust_ind.merge(df_freq, how="left", on="customer_id").fillna(0)

    if df_freq.customer_id.nunique() != len(unq_ids):

        warnings.warn(
            f"There are unmatched customers after aggregating at the invoice level."
        )

    return df_freq


def get_time_inactive(df_cust, ref_date):
    """
    Takes in a customer dataframe and
    returns the time since a customer
    made a purchase.
    
    Parameters:
    -----------
    
    df_cust : dataframe
    
    Customer dataframe
    
    ref_date : str
    
    Reference date to calculate the
    lifetime from
    
    Returns:
    --------
    
    df_out : dataframe
    
    Dataframe of customers including
    the lifetime
    
    """

    df_out = df_cust.copy()

    # Convert date to datetime
    ref_date = datetime.strptime(ref_date, "%Y-%m-%d %H:%M:%S")

    # Find the difference in days
    df_out["last_purchase"] = pd.to_datetime(
        df_out["last_purchase"], format="%Y-%m-%d %H:%M:%S"
    )
    df_out["time_inactive"] = (ref_date - df_out["last_purchase"]).astype(
        "timedelta64[s]"
    )
    df_out["time_inactive"] = (df_out["time_inactive"] / (24 * 3600)).round(1)

    return df_out


def get_customer_rates(df_cust):

    """
    Takes in a customer dataframe
    and calculates the following 
    rates:

    Order Spend Rate
    Quantity Spend Rate
    Quantity Rate

    Parameters:
    -----------

    df_cust : dataframe

    The customer dataframe

    Returns:
    --------

    df_out : dataframe

    Dataframe with the rates
    calculates

    """

    df_out = df_cust.copy()

    # Calculate all rates and return
    # the final dataframe
    df_out["ord_spend_rate"] = df_out["total_spend"] / df_out["orders"]
    df_out["quant_spend_rate"] = df_out["total_spend"] / df_out["quantity"]
    df_out["quant_rate"] = df_out["quantity"] / df_out["orders"]

    return df_out


def process_customer_data(df_cust, df_inv):
    """
    Takes in the customer dataframe
    and process it by creating new
    features that analyse customer
    behavior.
    
    Parameters:
    -----------
    
    df_inv : dataframe
    
    Dataframe with all invoices
    
    df_cust : dataframe
    
    Dataframe with all customers
    
    """

    # Make copies for all dataframes
    df_out = df_cust.copy()
    invoices = df_inv.copy()

    # Get the start and end date of all invoices
    ref_date = invoices.invc_date.max()
    start_date = invoices.invc_date.min()

    df_out = get_purchase_freq(df_inv=invoices, df_cust=df_out)

    df_out = get_customer_lifetime(
        df_cust=df_out, ref_date=ref_date, start_date=start_date
    )

    df_out = get_time_inactive(df_cust=df_out, ref_date=ref_date)

    df_out = get_customer_rates(df_cust=df_out)

    return df_out

import numpy as np
import pandas as pd
import re
from helper_funcs import *
from sklearn.model_selection import train_test_split


def add_col(jobs_df, spaced_name):
    spaced_name_lower = spaced_name
    possible_name_list = [spaced_name_lower]
    if spaced_name_lower.count(" ") > 0:
        # If the name has a space, replace with no space, then dash
        possible_name_list.append(spaced_name_lower.replace(" ", ""))
        possible_name_list.append(spaced_name_lower.replace(" ", "-"))
        
    contains_regex = "(?i)" + "|".join(possible_name_list)
    jobs_df[spaced_name] = jobs_df["Job Description"].str.contains(contains_regex)


def get_df():
    # Read csv as a df and drop NAs
    jobs_df = pd.read_csv("all_jobs.csv", usecols=range(1,16))

    # Drop rows that have important values as na
    jobs_df = jobs_df[jobs_df["Job Description"].notna()]
    jobs_df = jobs_df[jobs_df["Salary Estimate"].notna()]
    jobs_df = jobs_df[jobs_df["Size"].notna()]
    jobs_df = jobs_df[jobs_df["Location"].notna()]

    # Add columns for the technologies that the job postings include in their description
    qual_list = get_quals("qualifications.txt")

    for qual in qual_list:
        add_col(jobs_df, qual)
    
    # These two are weird with formatting so add manually
    # Scikit learn
    possible_name_list = ["Scikit learn", "Sci-kit learn", "Sci-kit-learn", "Scikit-learn"]
    contains_regex = "(?i)" + "|".join(possible_name_list)
    jobs_df["Scikit learn"] = jobs_df["Job Description"].str.contains(contains_regex)
    # R
    possible_name_list = [" R ", " R, "]
    contains_regex = "(?i)" + "|".join(possible_name_list)
    jobs_df["R"] = jobs_df["Job Description"].str.contains(contains_regex)

    return jobs_df


# Find average of two ranged numbers
def average_item(item):
    int_list = re.findall('\d+', item)
    int_list = [int(i) for i in int_list]
    return 1000 * sum(int_list) / len(int_list)


def get_estimate_values(jobs_df, col_name):
    jobs_df.drop(jobs_df[jobs_df[col_name] == "Unknown"].index, inplace = True)
    jobs_df.drop(jobs_df[jobs_df[col_name] == "-1"].index, inplace = True)
    jobs_df[col_name] = np.vectorize(average_item)(jobs_df[col_name])


def drop_other_cols(jobs_df):
    jobs_df.drop("Job Title", axis=1, inplace=True)
    jobs_df.drop("Job Description", axis=1, inplace=True)
    jobs_df.drop("Rating", axis=1, inplace=True)
    jobs_df.drop("Company Name", axis=1, inplace=True)
    jobs_df.drop("Headquarters", axis=1, inplace=True)
    jobs_df.drop("Founded", axis=1, inplace=True)
    jobs_df.drop("Type of ownership", axis=1, inplace=True)
    jobs_df.drop("Industry", axis=1, inplace=True)
    jobs_df.drop("Sector", axis=1, inplace=True)
    jobs_df.drop("Revenue", axis=1, inplace=True)
    jobs_df.drop("Competitors", axis=1, inplace=True)
    jobs_df.drop("Easy Apply", axis=1, inplace=True)


def location_to_state(jobs_df):
    # Turn last two characters of location to state. Most are formatted like this
    jobs_df["State"] = jobs_df["Location"].str[-2:]
    # Fix locations that aren't formatted normally
    # Single state endings
    jobs_df.loc[jobs_df["State"] == "te", "State"] = "RT"
    jobs_df.loc[jobs_df["State"] == "is", "State"] = "IL"
    jobs_df.loc[jobs_df["State"] == "ey", "State"] = "NJ"
    jobs_df.loc[jobs_df["State"] == "do", "State"] = "CO"
    jobs_df.loc[jobs_df["State"] == "ah", "State"] = "UH"
    jobs_df.loc[jobs_df["State"] == "an", "State"] = "MI"
    jobs_df.loc[jobs_df["State"] == "co", "State"] = "NM"
    # Multiple state endings
    jobs_df.loc[jobs_df["Location"] == "Maryland", "State"] = "MD"
    jobs_df.loc[jobs_df["Location"] == "Rhode Island", "State"] = "RD"
    jobs_df.loc[jobs_df["Location"] == "Georgia", "State"] = "GA"
    jobs_df.loc[jobs_df["Location"] == "Pennsylvania", "State"] = "PA"
    jobs_df.loc[jobs_df["Location"] == "California", "State"] = "CA"
    jobs_df.loc[jobs_df["Location"] == "Virginia", "State"] = "VA"
    jobs_df.loc[jobs_df["Location"] == "West Virginia", "State"] = "WV"
    jobs_df.loc[jobs_df["Location"] == "Arizona", "State"] = "AZ"
    jobs_df.loc[jobs_df["Location"] == "Indiana", "State"] = "IN"
    jobs_df.loc[jobs_df["Location"] == "Lousiana", "State"] = "LA"
    jobs_df.loc[jobs_df["Location"] == "Montana", "State"] = "MT"
    jobs_df.loc[jobs_df["Location"] == "North Carolina", "State"] = "NC"
    jobs_df.loc[jobs_df["Location"] == "South Carolina", "State"] = "SC"
    jobs_df.loc[jobs_df["Location"] == "Connecticut", "State"] = "CT"
    jobs_df.loc[jobs_df["Location"] == "Minnesota", "State"] = "MN"
    jobs_df.loc[jobs_df["Location"] == "North Dakota", "State"] = "ND"
    jobs_df.loc[jobs_df["Location"] == "South Dakota", "State"] = "SD"
    jobs_df.loc[jobs_df["Location"] == "Oklahoma", "State"] = "OK"
    jobs_df.loc[jobs_df["Location"] == "Alabama", "State"] = "AL"
    jobs_df.loc[jobs_df["Location"] == "Massachusetts", "State"] = "MA"
    jobs_df.loc[jobs_df["Location"] == "Arkansas", "State"] = "AR"
    jobs_df.loc[jobs_df["Location"] == "Kansas", "State"] = "KS"
    jobs_df.loc[jobs_df["Location"] == "Texas", "State"] = "TX"
    jobs_df.loc[jobs_df["Location"] == "Oregon", "State"] = "OR"
    jobs_df.loc[jobs_df["Location"] == "Washington", "State"] = "WA"
    # Drop values that we don't want
    jobs_df.drop(jobs_df[jobs_df['State'] == "da"].index, inplace = True)  # Canada
    jobs_df.drop(jobs_df[jobs_df['State'] == "io"].index, inplace = True)  # Ontario
    jobs_df.drop(jobs_df[jobs_df['State'] == "es"].index, inplace = True)  # No State
    jobs_df.drop(jobs_df[jobs_df['State'] == "om"].index, inplace = True)  # None?
    # Drop Location
    jobs_df.drop("Location", axis=1, inplace=True)


def train_test_split_jobs(jobs_df, test_size=0.20):
    X = jobs_df[jobs_df.columns.difference(["Salary Estimate"])]
    y = jobs_df["Salary Estimate"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    return X_train, X_test, y_train, y_test, X, y
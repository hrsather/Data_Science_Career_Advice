import pandas as pd
import numpy as np 


def add_col(jobs_df, spaced_name):
    spaced_name_lower = spaced_name
    possible_name_list = [spaced_name_lower]
    if spaced_name_lower.count(" ") > 0:
        # If the name has a space, replace with no space, then dash
        possible_name_list.append(spaced_name_lower.replace(" ", ""))
        possible_name_list.append(spaced_name_lower.replace(" ", "-"))
        
    contains_regex = "(?i)" + "|".join(possible_name_list)
    print(contains_regex)
    jobs_df[spaced_name] = jobs_df["Job Description"].str.contains(contains_regex)


def get_df():
    # Read csv as a df and drop NAs
    jobs_df = pd.read_csv("all_jobs.csv", usecols=range(1,16))
    jobs_df = jobs_df.dropna()  # TODO just drop needed cols

    print(jobs_df.head())
    
    # Add columns for the technologies that the job postings include in their description
    technology_list = []
    with open("technologies.txt") as tech_file:
        technology_list = tech_file.read().splitlines()

    for technology in technology_list:
        add_col(jobs_df, technology)
    
    # These two are weird with formatting so add manually
    # Scikit learn
    possible_name_list = ["Scikit learn", "Sci-kit learn", "Sci-kit-learn", "Scikit-learn"]
    contains_regex = "(?i)" + "|".join(possible_name_list)
    jobs_df["Scikit learn"] = jobs_df["Job Description"].str.contains(contains_regex)
    # R
    possible_name_list = [" R ", " R, "]
    contains_regex = "(?i)" + "|".join(possible_name_list)
    jobs_df["R"] = jobs_df["Job Description"].str.contains(contains_regex)

    # Turn location into just state
    jobs_df["State"] = jobs_df["Location"].str[-2:]

    # Remove "Glassdoor est." from Salary Estimate
    jobs_df["Salary Estimate"] = jobs_df["Salary Estimate"].str[:-17]

    # Drop description and unneeded cols
    jobs_df.drop("Location", axis=1, inplace=True)
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
    
    # Make dummie variables for size
    jobs_df = pd.get_dummies(jobs_df, columns=["Size"])

    return jobs_df


def main():
    jobs_df = get_df()
    print(list(jobs_df.columns))
    
    mask = np.random.rand(len(jobs_df)) < 0.8
    train_df = jobs_df[mask]
    test_df = jobs_df[~mask]

    print(train_df.head())
    print(train_df.shape)

    print(test_df.head())
    print(test_df.shape)



if __name__ == "__main__":
    main()
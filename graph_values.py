import matplotlib.pyplot as plt


def sort_col_to_arrays(jobs_df, column_name):
    x_counts = []
    x_names = []
    for name in jobs_df[column_name].unique():
        num_counts = len(jobs_df[jobs_df[column_name] == name])
        x_counts.append(num_counts)
        x_names.append(name)
    # Sort two columns for sorted graphing
    zipped_lists = zip(x_counts, x_names)
    sorted_pairs = sorted(zipped_lists, reverse=True)
    tuples = zip(*sorted_pairs)
    x_counts, x_names = [list(tuple) for tuple in tuples]
    # Get 10 largest
    x_counts = x_counts[:10]
    x_names = x_names[:10]

    return x_counts, x_names


def states_bar(jobs_df):
    state_counts, state_names = sort_col_to_arrays(jobs_df, "State")
    plt.bar(x=state_names, height=state_counts)
    plt.title("Histogram of States")
    plt.xlabel("States")
    plt.ylabel("Number of Occurances")
    plt.show()


def salary_hist(jobs_df):
    plt.hist(jobs_df["Salary Estimate"], bins=30)
    plt.title("Histogram of Salary")
    plt.xlabel("Salary")
    plt.ylabel("Number of Occurances")
    plt.show()


def size_graph(jobs_df):
    labels, counts = sort_col_to_arrays(jobs_df, "Size")
    plt.plot(labels, counts)
    plt.title("Number of Companies at different sizes")
    plt.xlabel("Size of Companies")
    plt.ylabel("Number of Companies at Size")
    plt.show()


def tech_occurs(jobs_df):
    technology_list = []
    count_list = []
    with open("qualifications.txt") as tech_file:
        technology_list = tech_file.read().splitlines()
        
    for tech in technology_list:
        count_list.append(jobs_df[tech].sum())

    zipped_lists = zip(count_list, technology_list)
    sorted_pairs = sorted(zipped_lists, reverse=True)
    tuples = zip(*sorted_pairs)
    x_counts, x_names = [list(tuple) for tuple in tuples]
    x_counts = x_counts[:10]
    x_names = x_names[:10]
        
    plt.figure(figsize=(10,5))
    plt.bar(x=x_names, height=x_counts)
    plt.title("Tech Occurances")
    plt.xlabel("Technology")
    plt.ylabel("Number of Occurances")
    plt.show()
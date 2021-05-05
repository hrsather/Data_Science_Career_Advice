import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from helper_funcs import *


def predict_salary(regr, candidate_row):
    return round(regr.predict([candidate_row])[0], 2)


def get_candidate_row(X, company_size):
    candidate_list = get_quals("applicant.txt")
    candidate_row = []
    for col in X.columns:
        if col == "Size":
            candidate_row.append(company_size)
        else:
            candidate_row.append(col in candidate_list)
    return candidate_row


def qualifications_to_salary(X, regr, company_size=5000):
    # Fill in applicants qualifications
    candidate_row = get_candidate_row(X, company_size=company_size)
    # Predict salary
    pred_sal = predict_salary(regr, candidate_row)
    return pred_sal


def size_effect(X, regr):
    salary_list = []
    size_list = []
    for size in range(1, 10000001, 1000):
        salary = qualifications_to_salary(X, regr, company_size=size)
        salary_list.append(salary)
        size_list.append(size)
    plt.plot(size_list, salary_list)
    plt.title("Effect of Number of Employees in Company to Size")
    plt.ylabel("Expected Salary")
    plt.xlabel("Number of employees at company")


def get_state_cols(X):
    state_cols = []
    for col_name in X.columns:
        if col_name[:5] == "State":
            state_cols.append(col_name)
    return state_cols


def get_non_state_cols(X):
    state_cols = []
    for col_name in X.columns:
        if col_name[:5] != "State":
            state_cols.append(col_name)
    return state_cols


def set_cols_to_false(X, state_cols, candidate_row):
    for i in range(len(X.columns)):
        col_name = X.columns[i]
        if col_name in state_cols:
            candidate_row[i] = False


def set_col_to_true(state_name, X, candidate_row):
    index = 0
    for i in range(len(X.columns)):
        col_name = X.columns[i]
        if col_name == state_name:
            index = i
            break
    candidate_row[index] = True


def sort_vals(x_names, x_counts, top_n=10, top=True):
    # Sort two columns for sorted graphing
    zipped_lists = zip(x_counts, x_names)
    sorted_pairs = sorted(zipped_lists, reverse=True)
    tuples = zip(*sorted_pairs)
    x_counts, x_names = [list(tuple) for tuple in tuples]
    # Get 10 largest
    if top:
        x_counts = x_counts[:top_n]
        x_names = x_names[:top_n]
    else:
        x_counts = x_counts[-top_n:]
        x_names = x_names[-top_n:]

    return x_names, x_counts


def state_effects(X, regr, starting_salary, top=True):
    state_cols = get_state_cols(X)
    candidate_row = get_candidate_row(X, 5000)
    state_list = []
    salary_list = []
    # Iterate through each different state
    for state_name in state_cols:
        set_cols_to_false(X, state_cols, candidate_row)
        set_col_to_true(state_name, X, candidate_row)
        salary = predict_salary(regr, candidate_row)
        salary_list.append(salary - starting_salary)
        state_list.append(state_name[-2:])

    state_list, salary_list = sort_vals(state_list, salary_list, top=top)
    plt.bar(state_list, salary_list)
    plt.title("Expected salary in different states")
    plt.xlabel("States")
    plt.ylabel("Salary")
    plt.show()


def qualifications_effects(X, regr, starting_salary, top=True):
    non_state_cols = get_non_state_cols(X)
    candidate_row = get_candidate_row(X, 5000)
    qual_list = []
    salary_list = []
    # Iterate through each different qualification
    for qual_name in non_state_cols:
        set_cols_to_false(X, non_state_cols, candidate_row)
        set_col_to_true(qual_name, X, candidate_row)
        salary = predict_salary(regr, candidate_row)
        salary_list.append(salary - starting_salary)
        qual_list.append(qual_name)

    qual_list, salary_list = sort_vals(qual_list, salary_list, top=top)
    plt.bar(qual_list, salary_list)
    plt.title("Expected salary with different qualfifications")
    plt.xlabel("Qualifications")
    plt.xticks(rotation=90)
    plt.ylabel("Salary")
    plt.show()
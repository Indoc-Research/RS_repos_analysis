import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import ast


def str2series(row, to_drop):
    info_tuple = ast.literal_eval(row)
    commits = info_tuple[0]
    metadata = info_tuple[1]
    for key in to_drop:
        metadata.pop(key, None)
    try:
        metadata["license"] = metadata["license"]["name"]
    except TypeError:
        metadata["license"] = None
    metadata["commits_on_default"] = commits
    return pd.Series(metadata)


def str_to_int_or_nan(a):
    try:
        return int(a)
    except ValueError:
        return np.nan


input_folder = "../../rs_usage/info_repos/"
files = [join(input_folder, f) for f in listdir(input_folder) if isfile(join(input_folder, f))]
files = [f for f in files if f.endswith(".csv")]

param_to_drop = ["owner", "permissions", "organization", "custom_properties", "template_repository", "parent", "source"]

df_list = []
for file in files:
    df = pd.read_csv(file)
    df.set_index("Unnamed: 0", inplace=True)
    df["to_drop"] = df["github_repo"].apply(lambda x: True if x == '(nan, nan)' else False)
    df = df[df["to_drop"] == False]
    metadata = df["github_repo"].apply(str2series, to_drop=param_to_drop)
    df_list.append(metadata)

metadata_df = pd.concat(df_list)
metadata_df.to_csv(f"{input_folder}/metadata/metadata.csv")
print()
import pandas as pd
from os import listdir
from os.path import isfile, join
import ast

input_folder = "../../rs_usage/info_repos/release_number/"
files = [join(input_folder, f) for f in listdir(input_folder) if isfile(join(input_folder, f))]
files = [f for f in files if f.endswith(".csv")]


def str2list(a):
    if a == "Error: Unable to retrieve release for url. Status code: 404":
        return 0
    else:
        return ast.literal_eval(a)


def clean_str(a):
    try:
        return int(a)
    except ValueError:
        return 0



df_list = []
for file in files:
    df = pd.read_csv(file)
    df["url"] = df["url"].apply(clean_str)
    df.set_index("Unnamed: 0", inplace=True)
    df_list.append(df)

metadata_df = pd.concat(df_list)
metadata_df.to_csv(f"{input_folder}/release_number.csv")

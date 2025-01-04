import pandas as pd
from os import listdir
from os.path import isfile, join
import ast

input_folder = "../../rs_usage/info_repos/release/"
files = [join(input_folder, f) for f in listdir(input_folder) if isfile(join(input_folder, f))]
files = [f for f in files if f.endswith(".csv")]


def str2list(a):
    if a == "Error: Unable to retrieve README for url. Status code: 404":
        return []
    else:
        return ast.literal_eval(a)


df_list = []
for file in files:
    df = pd.read_csv(file)
    df["url"] = df["url"].apply(str2list)
    df.set_index("Unnamed: 0", inplace=True)
    df_list.append(df)

metadata_df = pd.concat(df_list)
metadata_df.to_csv(f"{input_folder}/release.csv")

import pandas as pd
from os import listdir
from os.path import isfile, join
from consts import PROCESSED_RELEASE_FILES_PATH, PROCESSED_DF_PATH

input_folder = PROCESSED_RELEASE_FILES_PATH
files = [join(input_folder, f) for f in listdir(input_folder) if isfile(join(input_folder, f))]
files = [f for f in files if f.endswith(".csv")]


def clean_str(a):
    """
    Returns the integer value of a string, or 0 if it is not a number. This only happens when the "404 - NOT FOUNT"
    error is encountered
    :param a:
    :return:
    """
    try:
        return int(a)
    except ValueError:
        return 0

if __name__ == "__main__":
    df_list = []
    for file in files:
        df = pd.read_csv(file)
        df["url"] = df["url"].apply(clean_str)
        df.set_index("Unnamed: 0", inplace=True)
        df_list.append(df)

    metadata_df = pd.concat(df_list)
    metadata_df.to_csv(f"{PROCESSED_DF_PATH}/release_number.csv")

import pandas as pd
from os import listdir
from os.path import isfile, join
from consts import PROCESSED_README_FILES_PATH, PROCESSED_DF_PATH

if __name__ == "__main__":
    input_folder = PROCESSED_README_FILES_PATH
    files = [join(input_folder, f) for f in listdir(input_folder) if isfile(join(input_folder, f))]
    files = [f for f in files if f.endswith(".csv")]

    df_list = []
    for file in files:
        df = pd.read_csv(file)
        df.set_index("Unnamed: 0", inplace=True)
        df_list.append(df)

    metadata_df = pd.concat(df_list)
    metadata_df.to_csv(f"{PROCESSED_DF_PATH}/readme.csv")

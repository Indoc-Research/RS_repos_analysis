import ast
import pandas as pd
from consts import PROCESSED_METADATA_PATH, RAW_DATASET_PATH

if __name__ == "__main__":

    dataset = pd.read_csv(f"{RAW_DATASET_PATH}metadata.tsv", sep="\t", low_memory=False)
    metadata = pd.read_csv(f"{PROCESSED_METADATA_PATH}/metadata.csv", low_memory=False)
    df_github = metadata.copy()
    df_pypi = dataset[dataset["source"] == "Pypi Index"]
    df_pypi["github_repo"] = df_pypi["github_repo"].apply(ast.literal_eval)
    df_pypi["github_url_str"] = df_pypi["github_repo"].apply(lambda lst: lst[0] if lst else None )
    pypi_repo_urls = set(df_pypi["github_url_str"].dropna())
    df_github["exists_in_pypi"] = df_github["html_url"].isin(pypi_repo_urls)
    df_github["language"] = metadata["language"]
    minimal_info = df_github[["name", "html_url", "exists_in_pypi", "language"]]
    minimal_info.to_csv("data/pip_repo_combo.csv")

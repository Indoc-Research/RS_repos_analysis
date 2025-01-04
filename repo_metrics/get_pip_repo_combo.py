import ast
import pandas as pd
import numpy as np

if __name__ == "__main__":

    dataset = pd.read_csv("../../rs_usage/data/metadata.tsv", sep="\t", low_memory=False)
    df_github = dataset[dataset["source"] == "Github API"]
    df_pypi = dataset[dataset["source"] == "Pypi Index"]
    df_pypi["github_repo"] = df_pypi["github_repo"].apply(ast.literal_eval)
    df_pypi["github_url_str"] = df_pypi["github_repo"].apply(lambda lst: lst[0] if lst else None )
    pypi_repo_urls = set(df_pypi["github_url_str"].dropna())
    df_github["exists_in_pypi"] = df_github["github_repo"].isin(pypi_repo_urls)
    minimal_info = df_github[["software_mention", "github_repo", "exists_in_pypi"]]
    minimal_info.to_csv("../data/pip_repo_combo.csv")

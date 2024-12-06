import requests
from utils import get_access_token
import pandas as pd
import numpy as np

def get_default_branch(repo, token):
    url = f"https://api.github.com/repos/{repo}"
    headers = {
        'Authorization': f'token {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('default_branch')
    else:
        raise Exception(f"Failed to fetch repository info: {response.status_code}, {response.text}")

def count_commits_on_branch(repo, branch, token):
    url = f"https://api.github.com/repos/{repo}/commits"
    headers = {
        'Authorization': f'token {token}'
    }
    params = {
        'sha': branch,
        'per_page': 1
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        commit_count = response.links['last']['url'].split('page=')[-1]
        return int(commit_count)
    else:
        raise Exception(f"Failed to fetch commits: {response.status_code}, {response.text}")


def get_commits_on_main(repo, token):
    name = repo.split("/")[-1]
    user = repo.split("/")[-2]
    repo = f"{user}/{name}"

    try:
        default_branch = get_default_branch(repo, token)
        commit_count = count_commits_on_branch(repo, default_branch, token)
        return commit_count
    except Exception as e:
        print(repo, str(e))
        return np.nan

if __name__ == "__main__":
    dataset = pd.read_csv("../data/metadata.tsv", sep="\t", low_memory=False)
    dataset_github = dataset[dataset["source"] == "Github API"]
    token = get_access_token("../")
    commits_df_list = []
    commits_df = pd.DataFrame(columns=["commits_n"])

    commits_df["commits_n"] = dataset_github["github_repo"].apply(get_commits_on_main, token=token)
    commits_df.to_csv("./data/commits_n.csv")


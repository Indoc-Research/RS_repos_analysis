import requests
from utils import get_access_token
import pandas as pd
import numpy as np
import time


def get_default_branch(repo, token):
    """
    Places a get request and retrieves the default branch of the repo
    :param repo: repo in form user/repo_name
    :param token: token for API
    :return:
    """
    url = f"https://api.github.com/repos/{repo}"
    headers = {
        'Authorization': f'token {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('default_branch')
    else:
        raise Exception(f"Failed to fetch repository info: {response.status_code}, {response.text}")


def count_commits_on_branch(repo, token, branch):
    """
    Places a get request and counts the number of commits on the given branch
    :param repo: repo in form user/repo_name
    :param token: token for API
    :param branch: which branch to compute the commit counts on
    :return:
    """
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


def get_repo_info(repo, token):
    """
    Gets the default branch and counts the number of commits
    :param repo: URL of the repo
    :param token: token for API
    :return:
    """
    name = repo.split("/")[-1]
    user = repo.split("/")[-2]
    repo = f"{user}/{name}"

    try:
        metadata = count_commits_on_branch(repo, token)
        default_branch = ""
        #TODO default_branch = read from metadata
        commit_count = count_commits_on_branch(repo, default_branch, token)
        return commit_count, metadata
    except Exception as e:
        print(repo, str(e))
        return np.nan


def get_repo_metadata(repo, token):
    url = f"https://api.github.com/repos/{repo}"
    headers = {
        'Authorization': f'token {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        metadata = response.json()
        return metadata
    else:
        raise Exception(f"Failed to fetch metadata: {response.status_code}, {response.text}")


if __name__ == "__main__":

    #while True:
    #    if request_count >= 4999:
    #        reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600)) - time.time()
    #        print(f"Rate limit reached. Waiting for {reset_time} seconds.")
    #        time.sleep(reset_time + 1)
    #        request_count = 0
#
    #    response = requests.get(url, headers=headers, params=params)
    #    request_count += 1


    dataset = pd.read_csv("../data/metadata.tsv", sep="\t", low_memory=False)
    dataset_github = dataset[dataset["source"] == "Github API"]
    token = get_access_token("../")
    repo_info_df = pd.DataFrame(columns=["commits_n"])

    #TODO check how tuple return is handled by apply
    repo_info_df["commits_n"], repo_info_df["metadata"] = dataset_github["github_repo"].apply(get_repo_info, token=token)

    repo_info_df.to_csv("./data/commits_n.csv")

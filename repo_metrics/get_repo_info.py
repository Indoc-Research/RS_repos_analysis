import requests
from utils import get_access_token
import pandas as pd
import numpy as np
import time
from consts import RAW_DATASET_PATH, PROCESSED_METADATA_FILES_PATH


def count_commits_on_branch(repo, branch, token):
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
    global request_count
    response = requests.get(url, headers=headers, params=params)
    request_count += 1
    if response.status_code == 200:
        commit_count = response.links['last']['url'].split('page=')[-1]
        return int(commit_count)
    else:
        raise Exception(f"Failed to fetch commits: {response.status_code}, {response.text}")


def get_repo_metadata(repo, token):
    """
    Fetches the metadata of the repo
    :param repo:
    :param token:
    :return:
    """
    global request_count

    url = f"https://api.github.com/repos/{repo}"
    headers = {
        'Authorization': f'token {token}'
    }
    response = requests.get(url, headers=headers)
    if request_count >= 4900:
        reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600)) - time.time()
        print(f"Rate limit reached. Waiting for {reset_time} seconds.")
        time.sleep(reset_time + 1)
        request_count = 0

    if response.status_code == 200:
        metadata = response.json()
        request_count += 1
        return metadata
    else:
        request_count += 1
        raise Exception(f"Failed to fetch metadata: {response.status_code}, {response.text}")


def get_repo_info(repo, token):
    """
    Gets the default branch and counts the number of commits
    :param repo: URL of the repo
    :param token: token for API
    :return:
    """
    global request_count
    try:
        name = repo.split("/")[-1]
        user = repo.split("/")[-2]
        repo = f"{user}/{name}"
    except Exception as e:
        print(repo, str(e))
        return np.nan, np.nan

    try:
        metadata = get_repo_metadata(repo, token)
        default_branch = metadata["default_branch"]
        commit_count = count_commits_on_branch(repo, default_branch, token)
        return commit_count, metadata
    except Exception as e:
        print(repo, str(e))
        request_count += 1
        return np.nan, np.nan




if __name__ == "__main__":

    request_count = 0
    token = get_access_token("./")

    url = f"https://api.github.com/repos/ELGarulli/neurokin" # Use a dummy repo, to fetch the initial request count
    headers = {
        'Authorization': f'token {token}'
    }
    response = requests.get(url, headers=headers)
    reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600)) - time.time()

    dataset = pd.read_csv(f"{RAW_DATASET_PATH}metadata.tsv", sep="\t", low_memory=False)
    dataset_github = dataset[dataset["source"] == "Github API"]

    repo_info_df = pd.DataFrame(columns=["commits_n", "metadata"])
    idxs = np.linspace(0, len(dataset_github), 10, endpoint=True, dtype=int)
    for i in range(len(idxs)-1):
        info = dataset_github["github_repo"].iloc[idxs[i]:idxs[i+1]].apply(get_repo_info,
                                                                       token=token)

        info.to_csv(f"{PROCESSED_METADATA_FILES_PATH}/info_{idxs[i + 1]}.csv")

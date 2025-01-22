import requests
import time
import pandas as pd
import numpy as np
from utils import get_access_token
from consts import PROCESSED_METADATA_PATH, PROCESSED_RELEASE_FILES_PATH

def get_repo_releases_number(url, token):
    print(f"processing {url}")
    url = f"{url}/releases"
    headers = {
        "Authorization": f"token {token}",
    }
    params = {
        'per_page': 1
    }
    global request_count

    response = requests.get(url, headers=headers, params=params)
    request_count += 1
    if request_count >= 4990:
        reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600)) - time.time()
        print(f"Rate limit reached. Waiting for {reset_time} seconds.")
        time.sleep(reset_time + 1)
        request_count = 0

    if response.status_code == 200:
        releases = response.json()
        if len(releases) == 0:
            return 0
        else:
            links = response.links
            if "last" in links:
                last_url = links["last"]["url"]
                last_page_str = last_url.split("page=")[-1]
                return int(last_page_str)
            else:
                return 1
    else:
        return f"Error: Unable to retrieve release for {url}. Status code: {response.status_code}"



if __name__ == "__main__":

    request_count = 0
    token = get_access_token("./")
    url = f"https://api.github.com/repos/ELGarulli/neurokin"
    headers = {
        'Authorization': f'token {token}'
    }
    response = requests.get(url, headers=headers)
    reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600)) - time.time()

    dataset_github = pd.read_csv(f"{PROCESSED_METADATA_PATH}metadata.csv", low_memory=False)

    idxs = np.linspace(0, len(dataset_github), 10, endpoint=True, dtype=int)
    idxs = idxs[3:]
    for i in range(len(idxs)-1):
        info = dataset_github["url"].iloc[idxs[i]:idxs[i+1]].apply(get_repo_releases_number,
                                                                       token=token)
        info.to_csv(f"{PROCESSED_RELEASE_FILES_PATH}/release_number_{idxs[i+1]}.csv", escapechar="~")

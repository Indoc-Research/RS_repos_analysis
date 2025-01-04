import requests
from utils import get_access_token
import time
import pandas as pd
import numpy as np
def get_repo_readme(url, token):
    print(f"processing {url}")
    url = f"{url}/readme"
    headers = {
        "Authorization": f"token {token}",
    }
    global request_count

    response = requests.get(url, headers=headers)
    request_count += 1
    if request_count >= 4990:
        reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600)) - time.time()
        print(f"Rate limit reached. Waiting for {reset_time} seconds.")
        time.sleep(reset_time + 1)
        request_count = 0

    if response.status_code == 200:
        readme_data = response.json()
        readme_content = requests.get(readme_data['download_url']).text
        return readme_content
    else:
        return f"Error: Unable to retrieve README for url. Status code: {response.status_code}"


if __name__ == "__main__":

    request_count = 0
    token = get_access_token("../")
    url = f"https://api.github.com/repos/ELGarulli/neurokin"
    headers = {
        'Authorization': f'token {token}'
    }
    response = requests.get(url, headers=headers)
    reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600)) - time.time()

    dataset_github = pd.read_csv("../../rs_usage/metadata/metadata.csv", low_memory=False)

    repo_info_df = pd.DataFrame(columns=["readme"])
    idxs = np.linspace(0, len(dataset_github), 10, endpoint=True, dtype=int)

    for i in range(len(idxs)-1):
        info = dataset_github["url"].iloc[idxs[i]:idxs[i+1]].apply(get_repo_readme,
                                                                       token=token)
        info.to_csv(f"../../rs_usage/info_repos/readme_{idxs[i+1]}.csv", escapechar="~")

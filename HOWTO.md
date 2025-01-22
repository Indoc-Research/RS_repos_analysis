# Dataset download
I used the CZ Software Mention dataset [[1]](#1) as a starting point for this analysis.
Since we are only interested in the analysis of repos from publication, 
we can use the curated dataset. I used the provided README to select the "linked" folder 
and analysed the "metadata.tsv" file, which contains the list of repos urls, mined from biomedical publications. 

# API calls and main repo dataset
The first script to execute is [get_repo_info.py](repo_metrics/get_repo_info.py).
Briefly, it takes care of selecting the portion of the dataset that came from GitHub, and calling the GitHub
API to retrieve the main metadata of each repo, plus the number of commits on the default branch.

**For this script to work one has to**:
- set the (input) RAW_DATASET_PATH and (output) PROCESSED_METADATA_FILES_PATH folders in the [consts.py](consts.py) file.
- require a personal token from GitHub to increase the allowed number of API requests (5K/h for single users). 
  And place it in a config.cfg file as: 
  - [ACCESS]
    token = XXXX
  
**The pipeline is**:
  - Calling to a known repo (I used one of mine) to fetch the current request count and set a timer 
  to avoid the rate limit.
  - opening the metadata.tsv file and selecting the rows that come from the "GitHub API" source.
  - for each repo it first retrieves the metadata, extracts the default branch (tipically "main" or "master") 
and then places a second API call to get the number of commits on that branch.
  - the results are saved in a new metadata file, with the additional columns "default_branch" 
and "commits_on_default_branch".

**NOTE on pagination**:
For some metrics, GitHub uses pagination. That means the API response is split in multiple pages, to get the content
one has to iterate through all the pages. However, in this case we are only interested in the number of commits. So
one workaround, is to set the per_page parameter to 1, and then look at the page count.

**NOTE on practicality**: as the rate limit is 5K/h, and we are making 2 calls per each repo, the script will take a 
while to run. Unstable WiFi connection might also crash the script. For this reason, I split the calls in 10 chunks, 
and save each file separately.

**NOTE on dataset completeness**: Since the CZ dataset's creation, some repos have been deleted or made private. So the
updated metadata file we create will have slightly fewer entries than the original one. (see following steps)

The second script to be called is construct_metadata_dataset.py. It takes care of:
- drops empty repos (deleted or private)
- drops parameters that are not of use, and were causing problems in the following scripts (not constant types)
- as every value returned is a string, it converts the string representation of a series in a series
- merges the 10 files into a single one


# Additional calls for README and releases
The following metrics are directly contained in the metadata dataset: commits, stars, forks, license, 
creation and update time. However, we have to make additional calls to the GitHub API to retrieve the README and releases.
The files to run are [get_readme.py](repo_metrics/get_readme_data.py) and [get_releases.py](repo_metrics/get_release_data.py).
They maintain the same logic of the previous script, concerning the waiting time and the pagination (for releases count).
Since we don't need to make calls to Git repos that are now deleted or private, we can use the updated metadata.csv file.

Again, because of the length of the acquisition, I split the calls in 10 chunks, and save each file separately. 
They are then assembled in, respectively [construct_readme_dataset.py](repo_metrics/construct_readme_data.py) and
[construct_releases_dataset.py](repo_metrics/construct_release_data.py).

Also for these scripts, the variables for paths are stored in the file [consts.py](consts.py).

# Construction of the "pip dataframe"
To analyse how many repos have an entry in PyPi, we simply had to process the raw dataframe, and compare which
repos' names appeared both in the GitHub and a PyPi portion of the dataset.
This is done in the [get_pip_repo_combo.py](repo_metrics/get_pip_repo_combo.py) script.


# Visualization
All the visualizations are done in the corresponding jupyter notebooks. If any one-off preprocessing is needed (for 
example to be able to work with a lightweight numpy array instead of the whole metadata dataset), the preprocessing
is done in the first cells of the notebook, commented out and the data are saved in the ./data folder.


# References

<a id="1">[1]</a> Istrate, Ana-Maria; Veytsman, Boris; Li, Donghui et al. (2022). 
CZ Software Mentions: A large dataset of software mentions in the biomedical
literature [Dataset]. Dryad. https://doi.org/10.5061/dryad.6wwpzgn2c
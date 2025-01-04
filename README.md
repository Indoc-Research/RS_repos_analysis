## Analysis of Research Software on GitHub
### Scope
We investigated the common usage of GitHub in the biomedical field. 

### Dataset
We used the CZ Software Mention dataset as a starting point for this analysis.
We downloaded specifically the linked folder and analysed the "metadata" file, which contains the list of repos urls, 
mined from biomedical publications. From the metadata we selected the portion of the dataset that came from GitHub.

### Metrics

We downloaded generic metadata (e.g. license type, creation and update time), number of commits
on default branch (main, master), README and releases info from each of the available repos.

### Results

**Lifespan**
We analyzed the difference between the date of creation of the repo, and the date of the last update.
- The majority of repos became inactive after a few months. 
- Surprisingly we retrieved few repos with
"negative lifespans". These rare cases can arise when the repo was forked or cloned so that it inherited 
the commit history, and was never updated again. So the "last push" results before the creation of the new repo.

**Commits** 
- The vast majority of repos only includes one single commit.
- There is a weach correlation between the lifespan and the number of commits on default branch.

**README**

We classified the README in: none, short (<1500 bytes), informative (between 1500 and 10000 bytes) 
and detailed (>10000 bytes). We then displayed the word cloud of the most represented words.

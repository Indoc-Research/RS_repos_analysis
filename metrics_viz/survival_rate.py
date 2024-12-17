import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

#input_file = "../../rs_usage/metadata/metadata.csv"
#metadata = pd.read_csv(input_file)
#metadata.set_index('Unnamed: 0', inplace=True)
#
#
#metadata['created_at'] = pd.to_datetime(metadata['created_at'], format='%Y-%m-%dT%H:%M:%SZ')
#metadata['pushed_at'] = pd.to_datetime(metadata['pushed_at'], format='%Y-%m-%dT%H:%M:%SZ')
#
#lifespan = metadata['pushed_at'] - metadata['created_at']
#lifespan_months = lifespan.dt.days / 30.436875
#with open('../data/lifespan_months.npy', 'wb') as f:
#    np.save(f, lifespan_months.values)

lifespan_months = np.load('../data/lifespan_months.npy')

#fig, ax = plt.subplots()
#ax.hist(lifespan_months, bins=50)
#plt.show()

from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

# Suppose you have an array `durations` with the number of months each repo lasted,
# and an array `event_observed` (True/1 if the repo ended, False/0 if still alive).
events = [True if x>24 else False for x in lifespan_months]
kmf = KaplanMeierFitter()
kmf.fit(lifespan_months, event_observed=events)

kmf.plot_survival_function()
plt.title("Survival Curve of Repositories")
plt.xlabel("Time (months)")
plt.ylabel("Survival Probability")
plt.show()

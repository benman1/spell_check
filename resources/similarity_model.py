import wget
from collections import Counter
from Levenshtein import editops
from pyxdameraulevenshtein import damerau_levenshtein_distance
import pandas as pd
import numpy as np


url = 'http://www.dcs.bbk.ac.uk/~ROGER/'
filenames = ['aspell.dat', 'wikipedia.dat']
for filen in filenames:
    wget.download(url + filen)

def read_misspelling(filename):
    with open(filename, 'r') as myfile:
        data=myfile.read().split('$')

    del data[0]
    return [d[:-1].split('\n') for d in data]

def behavioral_model():
    corrections = []
    for filen in filenames:
        misspelling = read_misspelling(filen)
        for mis in misspelling:
            for w in mis[1:]:
                c = dict(Counter([e[0] for e in editops(mis[0], w)]))
                corrections.append(c)

    df = pd.DataFrame(corrections)
    df = df.replace(np.nan, -1)
    df = df.groupby(['delete', 'insert', 'replace']).size().reset_index()
    cols = list(df.columns)
    cols[-1] = 'frequency'
    df.columns = cols

    df['likelihood'] = df['frequency'].apply(lambda x: float(x) / sum(df['frequency']))
    del df['frequency']
    df['edit_dist'] = df['replace'] + df['insert'] + df['delete']
    df = df[df['likelihood'] > 0.001] # we ignore very low frequencies
    df = df[df.edit_dist >= 1] # ... and exact matches
    # calculated again: 
    df['likelihood'] = df['frequency'].apply(lambda x: float(x) / sum(df['frequency']))
    del df['frequency']
    df = df.replace(-1, 0)
    df.to_csv('corrections.csv', index=False)

def distance2prob():
	corrections = []

	for filen in filenames:
		misspelling = read_misspelling(filen)
		for mis in misspelling:
			for w in mis[1:]:
				corrections.append(damerau_levenshtein_distance(mis[0], w))
	df = pd.DataFrame(corrections)
	cols = list(df.columns)
	cols[-1] = 'frequency'
	df.columns = cols

	count = np.histogram(df['frequency'], bins=[1,2,3,4,5,6,7])
	s = float(sum(count))
	probs = [float(f)/s for f in count]
	print(probs)


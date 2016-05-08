import pickle
from nested_dict import nested_dict


# 1. unigram frequencies
s = open('nhs_unigram.txt', 'r').read()

freqlist = s.split(', ')
freqdict = {}
for w in freqlist:
    word, freq = w.split(': ')
    freqdict[word[1:-1]] = freq

vsum = 0
for v in freqdict.values():
    vsum += int(v)

priors = {word: float(int(freq))/float(vsum) for (word, freq) in freqdict.iteritems()}
pickle.dump(freqdict, open('priors.p', 'wb'))


# 2. word similarity model
s = open('corrections.csv', 'r').read()
table = s.split('\n')
headers = table[0]
del table[0]
del table[-1]
modelmatch = nested_dict()

for t in table:
    vals = t.split(',')
    delete = float(vals[0])
    insert = float(vals[1])
    replace = float(vals[2])
    likelihood = float(vals[3])
    modelmatch[delete][insert][replace] = likelihood

pickle.dump(modelmatch.to_dict(), open('similarity_model.p', 'wb'))
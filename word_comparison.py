import cPickle as pickle
from Levenshtein import editops
from pyxdameraulevenshtein import damerau_levenshtein_distance
from collections import OrderedDict, Counter
from nested_dict import nested_dict
import werkzeug


def get_priors():
    ''' in some future version, this might use a different collection type 
    such as tuples or namedtuples for speedup'''
    frequencies = pickle.load(open("resources/priors.p", "rb"))
    return frequencies

def match_model(edit):
    '''Given an edit sequence, look up the likelihood'''
    modelmatch = nested_dict(pickle.load(open("resources/similarity_model.p", "rb")))
    keys = {'delete': 0.0, 'insert': 0.0, 'replace': 0.0}
    d = dict(Counter([e[0] for e in edit]))
    for k,v in d.iteritems():
        keys[k] = v
    p = modelmatch[keys['delete']][keys['insert']][keys['replace']]
    if isinstance(p, float):
        return p
    else:
        return 0

def wordsim1(word1, word2):
    '''return a similarity score for between the two words
    TODO: stem the words
    '''
    probs = [1, 0.7669349429912811, 0.1784037558685446,
             0.03386988598256204, 0.015090543259557344,
             0.004024144869215292, 0.001676727028839705]
    dist = damerau_levenshtein_distance(str(word1), str(word2))
    if dist<len(probs):
        return probs[dist]
    else:
        return 0


def wordsim2(word1, word2):
    '''return a similarity score for between the two words
    attempt to use a behavioral model of edit distances
    '''
    dist = damerau_levenshtein_distance(str(word1), str(word2))
    if dist > 3:
        return 0
    edit = editops(str(word1), str(word2))
    return match_model(edit)

def get_candidates(word):
    '''get a dictionary of similar words, plus a similarity score
    I normalise similarities * priors / sum(similarities). You could use a softmax as well. 
    '''
    freqs = get_priors()

    # If the word is contained in the supplied word list, return the word with a score of 1
    if word in freqs:
        return {word: 1}

    similarities = {}
    for w1,freq in freqs.iteritems():
        pab = wordsim1(w1, word)
        similarities[w1] = pab * freq

    maxlen = 50
    ordered = sorted(similarities, key=similarities.get, reverse=True)[:maxlen]
    return OrderedDict([(o,similarities[o]) for o in ordered])

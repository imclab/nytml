import gc, copy, random, tools, numpy, sklearn, datetime, time
from sklearn.feature_extraction.text import CountVectorizer

from datetime import date
from copy import deepcopy
from tools import get_polarity
import classifier_tools
from classifier_tools import BOW_predict, POS_predict, new_features
from classifier_tools import score_by_label, kfold_crossval, randomize

wrdcnt = [12, 24, 42, 99, 183, 267]
trnk = [10, 24, 50, 100, 255, 556, 1927]
plrty = [-0.1868, -0.0615, -0.0304, 0, 0.0147, 0.0346, 0.059, 0.1607]
eTime = [548, 2055, 5253, 10512, 20849, 30583, 63125, 149094, 342090]

s_codes = { 'opinion':0,'us':1,'world':2,'opinionator':3,'krugman':4, 
            'business':5,'thecaucus':6,'nyregion':7,'well':8, 'magazine':9 }

# discretize rec count
def discretize_r(r_count):
    if int(r_count) > 10: return 1
    else: return 0 

def discretize(v, cutoffs):
    n = len(cutoffs)
    for i in range(n): 
        if v <= cutoffs[i]: return i
    return n

def npa(iter_object): return numpy.array(iter_object)

# retrieve n-size sample from date range s to e
# return raw features and label data (X, Y)
def get_data(n, s, e, metadata=False):

    gc.enable() # turn on garbage collection
    pop, comments = tools.date_range_sample(n, s, e)
    print 'Loaded %d comments' % pop
    print 'Random sample of %d from date range' % n
    gc.collect()
    print 'Garbage Collection complete'

    features, metafeatures, labels, = [], [], []

    for c in comments:
        text = c['commentBody'] # text is the feature data
        features.append(text.encode('ascii','ignore'))
        labels.append(discretize_r(c['recommendationCount']))

        if metadata:
            c_sec = s_codes[c['section']]
            c_wc = discretize(int(c['wordcount']), wrdcnt)
            c_rnk = discretize(int(c['timeRank']), trnk)
            c_elp = discretize(int(c['elapsedTime']), eTime)
            c_pol = discretize(get_polarity(c['sentiment']), plrty)

            metafeatures.append([c_wc, c_rnk, c_elp, c_sec])

    print 'Extracted text (features) and class labels'
    if not metadata: return (features, labels)
    else: return (features, metafeatures, labels)

def multistage_classify(n, s, e, folds):
    features, metafeatures, labels = get_data(n, s, e, metadata=True)
    features2 = new_features(features, labels, metafeatures)
    return kfold_crossval(npa(features2), npa(labels), folds, 2)
    
def classify_text(n, s, e, folds):

    features, labels = get_data(n, s, e)
    # POS_features = classifier_tools.POS_vectorize(features)
    # print 'Finished Part of Speech Tagging'
    # v = CountVectorizer(ngram_range=(1,2), token_pattern=r'\b\w+\b', min_df=1)
    # v_features = (v.fit_transform(POS_features)).toarray()
    # transform text into count vectors
    v = CountVectorizer(min_df=1, max_features=2000)
    v_features = (v.fit_transform(features)).toarray()
    print 'Finished vectorizing text data'

    X, Y = randomize(v_features, labels)

    print len(X[0])

    if len(X) == len(Y): print 'Data check ... OK'
    else: 
        print 'Data check failed. Aborting execution'
        return None

    return kfold_crossval(X, Y, folds, 2, RF=True)

def iterateMNB(n_trials, d_range, s_size, folds):

    C0L, C1L, WL = [], [], []
    # upper and lower date limits
    ll = datetime.date(2012,01,01)
    ul = datetime.date(2013,06,01)

    v = CountVectorizer(min_df=1, max_features=2000)

    for i in range(n_trials):
        s = tools.randomDate(ll, ul)
        e = date.fromordinal(s.toordinal() + d_range)
        # c0, c1, w = multistage_classify(s_size, s, e, folds)
        c0, c1, w = classify_text(s_size, s, e, folds)
        C0L.append(c0); C1L.append(c1); WL.append(w)
        
    print 'mean class-0 accuracy (recall) score : %0.3f' % (npa(C0L)).mean()
    print 'mean class-1 accuracy (recall) score : %0.3f' % (npa(C1L)).mean()
    print 'mean weighted accuracy (recall) score : %0.3f' % (npa(WL)).mean()

start_time = time.clock()
iterateMNB(10, 4, 10000, 2)
elapsed = time.clock() - start_time
print 'Elapsed time: %f' % elapsed

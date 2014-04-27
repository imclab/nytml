import gc, copy, random, tools, numpy, sklearn, datetime, time
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from datetime import date
from copy import deepcopy
import classifier_tools
from classifier_tools import score_by_label, kfold_crossval, randomize

# discretize rec count
def discretize(r_count):
    if int(r_count) > 10: return 1
    else: return 0 

def npa(iter_object): return numpy.array(iter_object)

# retrieve n-size sample from date range s to e
# return raw features and label data (X, Y)
def get_data(n, s, e):

    gc.enable() # turn on garbage collection
    pop, comments = tools.date_range_sample(n, s, e)
    print 'Loaded %d comments' % pop
    print 'Random sample of %d from date range' % n
    gc.collect()
    print 'Garbage Collection complete'

    features, labels = [], []

    for c in comments:
        text = c['commentBody'] # text is the feature data
        features.append(text.encode('ascii','ignore'))
        labels.append(discretize(c['recommendationCount']))

    print 'Extracted text (features) and class labels'

    return (features, labels)

def classify_text(n, s, e, folds, vrz):

    features, labels = get_data(n, s, e)
    
    POS_features = classifier_tools.POS_vectorize(features)
    print 'Finished Part of Speech Tagging'
    v_features = (vrz.fit_transform(POS_features)).toarray()

    # transform text into count vectors
    # v_features = (vrz.fit_transform(features)).toarray()
    print 'Finished vectorizing text data'

    X, Y = randomize(v_features, labels)

    print len(X[0])

    if len(X) == len(Y): print 'Data check ... OK'
    else: 
        print 'Data check failed. Aborting execution'
        return None

    return kfold_crossval(X, Y, folds, 2)

    """ 
    MNB = MultinomialNB()
    # MNB = RandomForestClassifier()

    MNB2 = MultinomialNB()
    MNB2.fit(npa(X), npa(Y))
    Y_Pred = MNB2.predict(npa(X))

    print 'Classifier Accuracy'
    results = score_by_label(Y, Y_Pred, 2)
    print results

    return classification_report(npa(Y), Y_Pred)
    # print 'MNB Accuracy: %0.2f (+/- %0.2f)' % results
    """


def iterateMNB(n_trials, d_range, s_size, folds):

    C0L, C1L, WL = [], [], []

    # upper and lower date limits
    ll = datetime.date(2012,01,01)
    ul = datetime.date(2013,06,01)
    
    v = CountVectorizer(ngram_range=(1,2),token_pattern=r'\b\w+\b', min_df=1)
    # v = TfidfVectorizer(min_df=1)

    for i in range(n_trials):
        s = tools.randomDate(ll, ul)
        e = date.fromordinal(s.toordinal() + d_range)
        c0, c1, w = classify_text(s_size, s, e, folds, v)
        C0L.append(c0); C1L.append(c1); WL.append(w)

    print 'mean class-0 accuracy (recall) score : %0.3f' % (npa(C0L)).mean()
    print 'mean class-1 accuracy (recall) score : %0.3f' % (npa(C1L)).mean()
    print 'mean weighted accuracy (recall) score : %0.3f' % (npa(WL)).mean()
    
start_time = time.clock()
iterateMNB(10, 3, 5000, 2)
elapsed = time.clock() - start_time
print 'Elapsed time: %f' % elapsed

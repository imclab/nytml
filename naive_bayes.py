import gc, copy, random, tools, numpy, sklearn, datetime, time
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


from datetime import date

# print scores for each label given true vals, predicted vals
def label_score(Y, Y_Pred, n_labels):

    counts, correct = {}, {}
    labels = range(n_labels)
    for label in labels:
        counts[label], correct[label] = 0, 0

    for i in range(len(Y)):

        true = int(Y[i])
        predicted = int(Y_Pred[i])

        for j in labels:
            if true == j:
                counts[j] += 1
                if predicted == j:
                    correct[j] += 1
    
    for k in labels:
        x, y = counts[k], correct[k]
        values = (k, x, y, float(y) / float(x))
        print 'Class %d: count = %d, correct = %d, score = %0.3f' % values

# discretize recommendation count
def discretize_r(r_count):
    if int(r_count) > 10: return 1
    else: return 0 

def npa(iter_object): return numpy.array(iter_object)

def classify_text(n, s, e, folds, vrz):

    cls_label = 'recommendationCount'
    gc.enable() # turn on garbage collection
    pop, comments = tools.date_range_sample(n, s, e)
    print 'Loaded %d comments' % pop
    print 'Selected random sample of size %d from date range' % n
    gc.collect()
    print 'Garbage Collection complete'

    features, labels = [], []

    # extract text and desired label
    for c in comments:
        text = c['commentBody'] # text is the feature data
        label = discretize_r(c['recommendationCount'])
        labels.append(label)
        features.append(text.encode('utf8','ignore'))

    print 'Extracted text (features) and class labels'

    # transform text into count vectors
    v_features = (vrz.fit_transform(features)).toarray()

    print 'Finished vectorizing text data'

    random_indices = copy.deepcopy(range(len(labels)))
    random.shuffle(random_indices)
    X, Y = [], []

    for i in random_indices:
        Y.append(labels[i])
        X.append(v_features[i])

    if len(X) == len(Y): print 'Data check ... OK'
    else: 
        print 'Data check failed. Aborting execution'
        return None

    # MNB = RandomForestClassifier()
    MNB = MultinomialNB()
    kfold_m = (cross_val_score(MNB, npa(X), npa(Y), cv=folds)).mean()

    MNB2 = MultinomialNB()
    MNB2.fit(npa(X), npa(Y))
    Y_Pred = MNB2.predict(npa(X))
    
    label_score(Y, Y_Pred, 2)

    return (kfold_m, classification_report(npa(Y), Y_Pred))

    # print 'MNB Accuracy: %0.2f (+/- %0.2f)' % results

def processReport(report):
    l = report.split('\n')
    p0 = l[2].split()[1]
    p1 = l[3].split()[1]
    w_a = l[5].split()[3]
    return (p0, p1, w_a)

def iterateMNB(n_trials, d_range, s_size, folds, m_feat):

    KFS, WA, P1S = [], [], []

    # upper and lower date limits
    ll = datetime.date(2012,01,01)
    ul = datetime.date(2013,06,01)
    
    # v = CountVectorizer(min_df=1)
    v = TfidfVectorizer(min_df=1)

    for i in range(n_trials):
        s = tools.randomDate(ll, ul)
        e = date.fromordinal(s.toordinal() + d_range)
        kfm, report = classify_text(s_size, s, e, folds, v)

        print report
    
start_time = time.clock()
iterateMNB(2, 3, 5000, 5, 2000)
elapsed = time.clock() - start_time
print 'Elapsed time: %f' % elapsed

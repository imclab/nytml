import gc, copy, random, tools, numpy, sklearn, datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

test_factor = 10
pop_size, sample_size = 50000, 5000

# discretize sentiment into binary labels
def discretize_s(s_map):
    p, n = float(s_map['pos']), float(s_map['neg'])
    if p >= n: return 1
    else: return 0 

# discretize recommendation count
def discretize_r(r_count):
    if int(r_count) > 10: return 1
    else: return 0 

def npa(iter_object): return numpy.array(iter_object)

def classify_text(cls_label):

    if cls_label not in ['sentiment','recommendationCount']:
        print 'invalid class label'
        return None

    gc.enable() # turn on garbage collection
    comments = tools.load_n_comments(pop_size, start='2012-01-01')
    print 'Loaded ' + str(pop_size) + ' data points'
    comments = random.sample(comments[1], sample_size)
    print 'Selected random sample of size ' + str(sample_size) + ' from population'
    gc.collect()
    print 'Garbage Collection complete'

    features, labels = [], []

    # extract text and desired label
    for c in comments:

        text = c['commentBody'] # text is the feature data
        
        if cls_label == 'sentiment': 
            label = discretize_s(c['sentiment'])
        elif cls_label == 'recommendationCount' : 
            label = discretize_r(c['recommendationCount'])

        labels.append(label)
        features.append(text.encode('utf8','ignore'))

    print 'Extracted text (features) and class labels'

    v = CountVectorizer(min_df=1) # X -> feature data
    X = (v.fit_transform(features)).toarray()

    print 'Finished vectorizing text data'

    Y = npa(labels) # Y -> corresponding labels

    if len(X) == len(Y): print 'Data check 1...OK'
    else: 
        print 'Data check failed. Aborting execution'
        return None

    random_indices = copy.deepcopy(range(len(Y)))
    random.shuffle(random_indices)

    tst_n, trn_n = 0, 0
    trainX, testX, trainY, testY = [], [], [], []

    for i in random_indices:
        if tst_n < (Y.size / test_factor):
            testX.append(X[i])
            testY.append(Y[i])
            tst_n += 1
        else:
            trainX.append(X[i])
            trainY.append(Y[i])
            trn_n += 1

    print 'Randomly partitioned data into test and training sets'
    print 'Test set contains ' + str(tst_n) + ' data points'
    print 'Training set contains ' + str(trn_n) + ' data points'

    if (len(trainX) == len(trainY)) and (len(testX) == len(testY)): 
        print 'Data check 2...OK'
    else: 
        print 'Data check failed. Aborting'
        return None

    nb_classifier = MultinomialNB()
    nb_classifier.fit(npa(trainX), npa(trainY))
    
    results = str(nb_classifier.score(npa(testX), npa(testY)))

    print 'accuracy of Multinomial Naive Bayes Classifier ' + results


print 'Performing Naive Bayes Classification w/ sentiment label'
classify_text('sentiment')

print ''

print 'Performing Naive Bayes Classification w/ recommendation count label'
classify_text('recommendationCount')



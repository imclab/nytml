import random
from textblob import TextBlob
from copy import deepcopy
from numpy import array
from sklearn.naive_bayes import MultinomialNB

# scores for each label given true vals, predicted vals
def score_by_label(Y, Y_Pred, n_labels):
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
    
    scores, weighted = {}, 0.0
    results = 'Class %d: count = %d, correct = %d, score = %0.3f'

    for k in labels:
        x, y = counts[k], correct[k]
        z = float(y) / float(x)
        print results % (k,x,y,z)

        scores[k] = z
        weighted += z * (float(x)/float(len(Y)))

    return (weighted, scores)

def partition(lst, n):
	return [deepcopy(lst[i::n]) for i in xrange(n)]

def unzip(zipped_list):
    try:
        x, y = zip(*zipped_list)
        return (array(x), array(y))
    except:
        print 'ERROR'
        print zipped_list
        return ([],[])

def randomize(l1, l2):
    if len(l1) != len(l2): return None
    X, Y = [], []
    rvals = deepcopy(range(len(l1)))
    random.shuffle(rvals)
    for i in rvals:
        X.append(l1[i])
        Y.append(l2[i])
    return (X, Y)

# X is the feature data, Y is the class label vector
def kfold_crossval(X, Y, k, n_labels):
    labels, size, lmap, kmap, = range(n_labels), len(Y), {}, {}
    for label in labels: lmap[label] = []
 
    # group by label
    for i in range(size): lmap[int(Y[i])] += [(X[i], Y[i])]
    # partition each label list into k parts
    for label in labels: kmap[label] = partition(lmap[label], k)
    
    results = []

    for j in range(k):
        test, train = [], []
        for label in labels:
            index = 0
            for kgroup in kmap[label]:
                if index == j: test += kgroup 
                else: train += kgroup
                index += 1
        x_test, y_test = unzip(test)
        x_train, y_train = unzip(train)

        MNB = MultinomialNB()
        MNB.fit(x_train, y_train)
        results.append(score_by_label(y_test, MNB.predict(x_test), n_labels))

    rlen, wsum, c0sum, c1sum = float(len(results)), 0.0, 0.0, 0.0
    for result in results:
        wght, cmap = result
        wsum += wght
        c0sum += cmap[0]
        c1sum += cmap[1]
    avg_vals = (c0sum / rlen, c1sum / rlen, wsum / rlen)
    return avg_vals
    # print '%d-fold validation results:' % k
    # print 'class-0 : %0.3f, class-1 : %0.3f, weighted : %0.3f' % avg_vals

def POS_vectorize(documents):
    OUT = []
    for document in documents:
        tokens, taglist = unzip((TextBlob(document)).tags)
        OUT.append(' '.join(taglist))
    return OUT

    """
    tokenized = map(nltk.word_tokenize, documents)
    tagged, OUT = nltk.batch_pos_tag(tokenized), []

    for sentence in tagged:
        tokens, tags = unzip(sentence)
        OUT.append(' '.join(tags))
    
    return OUT
    """

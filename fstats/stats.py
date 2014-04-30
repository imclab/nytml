import powerlaw
import numpy, scipy, math
from random import sample
from numpy import array
from scipy.stats import poisson, geom, norm
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge


def lg2(x):
    return math.log(int(x) + 1, 2)

def loadFeatures():

    cnt, thresh = 0, 1000000
    data, names = {}, ['id', 'recs', 'wc', 'pol', 'rnk', 'time', 'cls']

    for name in names: data[name] = []
    with open('features.tab', 'r') as f:
        for line in f:
            if line[0].isalpha(): continue
            linedata = line.split()
            for i in range(len(linedata)):
                data[names[i]].append(linedata[i])
            cnt += 1
            if (cnt % thresh) == 0: print cnt
    return (cnt, data)

def multi_var_OLS(sample_size, data, size, xarg='all', log=True):

    X, Y = [], []
    sample_indices = sample(range(size), sample_size)

    for i in sample_indices:

        Y.append(lg2((data['recs'])[i]))

        if log:
            xvals = [ lg2((data['wc'])[i]), 
                      lg2((data['time'])[i]), 
                      float((data['pol'])[i]) ]
        else:
            xvals = [ int((data['wc'])[i]), 
                      int((data['time'])[i]), 
                      float((data['pol'])[i]) ]

        if xarg == 'wc': X.append([xvals[0]])
        elif xarg == 'time': X.append([xvals[1]])
        elif xarg == 'pol' : X.append([xvals[2]])
        else: X.append(xvals)

    print 'Random Sample Crated'
    print 'Data is as follows, X[:5], Y[:5]', X[:5], Y[:5]

    reg = LinearRegression()
    reg.fit(X, Y)
    print 'Variance Score : %0.4f' % reg.score(X, Y)

    if xarg != 'all':
        plt.scatter(X, Y)
        plt.plot(X, reg.predict(X))
        plt.show()

def regression():
    n = 100000 # sample size
    data = loadFeatures()
    print 'features sucessfully loaded'
    y_s, x_s = [], []
    r_s = sample(xrange(len(data['recs'])), n)
    for j in r_s:
        r_v, w_v = int((data['recs'])[j]), int((data['wc'])[j])
        y_s.append(math.sqrt(r_v))
        x_s.append(math.sqrt(w_v))
    y_s, x_s = array(y_s, float), array(x_s, float)
    y, x = y_s.reshape(y_s.shape[0],-1), x_s.reshape(x_s.shape[0],-1)
    print 'data sampled and reshaped'
    reg = LinearRegression()
    reg.fit(x, y)
    print 'regression fitted'
    print 'variance score: ', reg.score(x, y)
    plt.scatter(x,y,color='b')
    plt.plot(x, reg.predict(x),color='red')
    plt.xlabel('Word Count (sqrt)')
    plt.ylabel('Recommendation Count (sqrt)')
    plt.suptitle('Ordinary Least Squares (OLS)')
    plt.show()

def pareto(data):
    n = len(data)
    print n
    def ln(x): return math.log(x+1)
    logdata = map(ln, data)
    alpha = float(n) / numpy.sum(logdata)
    print 'alpha parameter ', alpha
    ar = numpy.arange(2, 40)
    def ppdf(x): return (alpha / (math.pow(x,(alpha+1))))
    return (ar, map(ppdf, ar))

def recDistribution():
    data = loadFeatures()
    recs = array(data['recs'], float)
    mu = numpy.average(recs)
    print mu
    dist = poisson(mu)
    dist2 = geom((1.0/mu))
    dist3 = pareto(recs)
    x = numpy.arange(1, numpy.amax(recs))
    h = plt.hist(recs, bins=range(40), normed=True)
    plt.plot(dist3[0], dist3[1], color='yellow', label='Pareto', linewidth=3)
    plt.plot(x, dist.pmf(x), color='black', label='Poisson', linewidth=3)
    plt.plot(x, dist2.pmf(x), color='red', label='Geometric', linewidth=3)
    plt.legend()
    plt.xlabel('Recommendation Count')
    plt.ylabel('Actual Value (% of Data) / Probability')
    plt.legend()
    plt.suptitle('Fitting Rec. Count')
    plt.xlim(0,40)
    plt.show()

def sentiment_dist():
    data, dif = loadFeatures(), []
    pos = array(data['pos'], float)
    neg = array(data['neg'], float)
    pmean, pstd = norm.fit(pos)
    nmean, nstd = norm.fit(neg)
    print 'positive: mean, std: ', pmean, pstd
    print 'negative: mean, std: ', nmean, nstd    
    
    for i in range(len(pos)):
        dif.append(pos[i] - neg[i])
    dmean, dstd = norm.fit(dif)
    print 'delta: mean, std: ', dmean, dstd

import copy

""" parse sentiment wordnet (sentiword.txt) and create a 1-to-1
    mapping of words to sentiment values. words with more than one
    set of values for sentiment will simply take the average of all
    sentiment values provided for that word """

def parse():

    f = open('sentiword.txt', 'r')
    p, n, word, wmap = 2, 3, 4, {}

    for line in f:

        if line[0] == '#': continue
        else:

            ls = line.split('\t')
            words = ls[word].split()

            try: f_p, f_n = float(ls[p]), float(ls[n])
            except ValueError: continue

            val = {'pos':f_p,'neg':f_n}

            for w in words:
                term = (w.split('#'))[0]
                if term in wmap:
                    (wmap[term]).append(copy.deepcopy(val))
                else: 
                    wmap[term] = [copy.deepcopy(val)]

    f.close()

    def avgsent(ls):
        n, f_pos, f_neg = len(ls), 0.0, 0.0
        for i in range(n):
            f_pos += (ls[i])['pos']
            f_neg += (ls[i])['neg']
        f_pos, f_neg = f_pos / float(n), f_neg / float(n)
        return {'pos':f_pos,'neg':f_neg}

    for k in wmap.keys(): wmap[k] = avgsent(wmap[k])

    return wmap

parse()

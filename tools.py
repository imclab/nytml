import datetime, random, numpy, json, gc
from datetime import date
from copy import deepcopy

MIN_DATE = datetime.date(2005,1,1)
MAX_DATE = datetime.date(2014,1,1)

def date_from_yr(y): return datetime.date(y, 1, 1)

# increment date object d by one day
def incrementDate(d):
    return date.fromordinal((d.toordinal()+1))

# returns a random date between date s and date e
def randomDate(s, e):
    def f(y): return int((y.toordinal()))
    return date.fromordinal(random.randrange(f(s), f(e)))

# construct a date object from a string YYYY-MM-DD
def datefromISO(str_date):
    year, month, day = str_date.split('-')
    return datetime.date(int(year), int(month), int(day))

# retrieve a comment list from the file pointed to by date object d_obj
def get_comment_list(d_obj):
    try:
        f = open(str(d_obj.year) + '/' + d_obj.isoformat() + '.json', 'r')
        comment_list = json.load(f)
        f.close()
        return comment_list
    except ValueError: return []

def write_comment_list(d_obj, c_list):
    f = open(str(d_obj.year) + '/' + d_obj.isoformat() + '.json', 'w')
    json.dump(c_list, f)
    f.close()

# loads n comments from the dataset (2005 - 2013). 
# If date is unspecified then pick a random starting date. 
# If section is unspecified then load comments of any section
def load_n_comments(n, start=None, section=None):

    if start is not None: 
        start = datefromISO(start)
    else: start = randomDate(MIN_DATE, MAX_DATE)

    n, comments = int(n), []
    def bySection(c): return c['section'] == section

    while True:
        d_iso = start.isoformat()

        if cmp(start, MAX_DATE) == 0: 
            return (d_iso, comments)

        c = get_comment_list(start)

        if len(c) == 0:
            start = incrementDate(start)
            continue

        if section is not None: c = filter(bySection, c)
        comments.extend(c)

        c_len = len(comments)
        if c_len > n: return (d_iso, comments[:n])
        elif c_len == n: return (d_iso, comments)
        else: start = incrementDate(start)

def isString(s):
    return str(type(s)) == "<type 'str'>"

def isDate(d):
    return str(type(d)) == "<type 'datetime.date'>"

# n is sample size; s, e are iso-string dates
def date_range_sample(n, s, e, section=None):
    OUT = []
    gc.enable()

    if (isString(s) and isString(e)):
        start, end = datefromISO(s), datefromISO(e)
    elif (isDate(s) and isDate(e)): start, end = s, e
    
    while cmp(start, end) != 0:
        c = get_comment_list(start)
        OUT.extend(c)
        start = incrementDate(start)
    
    pop = len(OUT)
    if pop < n:
        print 'date range too narrow for', n
        print 'returning %d comments' % pop
        return (pop, OUT)
    else: return (pop, random.sample(OUT, n))

def get_polarity(sentiment):
    return (float(sentiment['pos']) - float(sentiment['neg']))

# traverse all comments
def traverse_all():
    gc.enable()
    s, e = MIN_DATE, MAX_DATE
    s_y = s.year

    f = open('features.tab', 'w+')
    nms = ['id', 'recs', 'wc', 
           'polar', 'rnk', 'time', 'cls']
    f.write('\t'.join(nms) + '\n')
    dtypes = ['c', 'c', 'c', 'c', 'c', 'c', 'd']
    f.write('\t'.join(dtypes) + '\n')
    flags = ['meta', '', '', '', '', '', 'class']
    f.write('\t'.join(flags) + '\n')

    while cmp(s, e) != 0:
        if s_y != s.year:
            print s_y
            s_y = s.year
            gc.collect()

        comments = get_comment_list(s)

        if len(comments) == 0:
            s = incrementDate(s)
            continue

        for comment in comments:
            print 'hello'
            # do something
            
        s = incrementDate(s)
    f.close()


"""
    OLD CODE
            if 'commentTitle' in comment: 
                del comment['commentTitle']
            comment['commentID'] = count_id
            
            if 'articleURL' in comment and 'approveDate' in comment:

                c_url = comment['articleURL']
                val = (count_id, comment['approveDate'])
                if c_url in urlmap:
                    urlmap[c_url].append(deepcopy(val))
                else: urlmap[c_url] = [deepcopy(val)]
    with open('url_timemap.json', 'w+') as f: json.dump(urlmap, f)

    OLD CODE
            # retrieve and parse data
            rec = str(cx['recommendationCount'])
            wcc = str(cx['wordcount'])
            snt = cx['sentiment']
            pos = str(round(float(snt['pos']), 3))
            neg = str(round(float(snt['neg']), 3))
            csq = str(cx['commentSequence'])            
            cdt = datetime.datetime.fromtimestamp(float(cx['approveDate']))
            wd = str(cdt.isoweekday())

            # write to file
            line = ' '.join([rec,wcc,pos,neg,csq,wd,str(cdt.hour)])
            f.write(line + '\n')
            count += 1
        s = incrementDate(s)
    print str(count) + ' comments traversed'
    f.close()

    OLD CODE
    sections = [] # store valid sections
    # retrieve valid sections from sections.txt
    with open('sections.txt', 'r') as ss:
        for ln in ss: sections.append(ln.split()[0])
    # function used to apply filter
    def byS(x): return x['section'] in sections
"""

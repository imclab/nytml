import datetime, random, numpy, json, gc
from datetime import date

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

# comapres two date objects at day-level granularity
def compareDate(d1, d2):
    n1, n2 = d1.toordinal(), d2.toordinal()
    if n1 < n2: return -1
    elif n1 == n2: return 0
    elif n1 > n2: return 1

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
        
# traverse all comments
def traverse_all():
    gc.enable() # enable garbage collector
    s, e, urlmap = MIN_DATE, MAX_DATE, {}

    s_y = s.year # starting year
    sections = [] # store valid sections

    # retrieve valid sections from sections.txt
    with open('sections.txt', 'r') as ss:
        for ln in ss: sections.append(ln.split()[0])

    # function used to apply filter
    def byS(x): return x['section'] in sections

    # file to write to
    # f, count = open('features', 'w+'), 0

    # f.write('# Legend: Recs Wc Pos Neg Seq DoW Hour\n')

    while cmp(s, e) != 0:

        # track progress & collect garbage
        if s_y != s.year:
            print s_y
            s_y = s.year
            gc.collect()

        # retrieve comments
        c = filter(byS, get_comment_list(s))
        write_comment_list(s, c) # write filtered list
        if len(c) == 0:
            s = incrementDate(s)
            continue

        for cx in c:
            
            """
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
    """

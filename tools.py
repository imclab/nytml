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

def get_comment_list(d_obj):
    try:
        f = open(str(d_obj.year) + '/' + d_obj.isoformat() + '.json', 'r')
        comment_list = json.load(f)
        f.close()
        return comment_list
    except ValueError:
        return []

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

        if cmp(start, MAX_DATE) == 0: return comments

        c = get_comment_list(start)

        if len(c) == 0:
            start = incrementDate(start)
            continue

        if section is not None: c = filter(bySection, c)
        comments.extend(c)

        c_len = len(comments)

        if c_len > n: return comments[:n]
        elif c_len == n: return comments
        else: start = incrementDate(start)
        
# traverse all comments from year s to year e
def traverse_all(s, e):
    gc.enable() # enable garbage collector
    s, e, urlmap = date_from_yr(s), date_from_yr(e), {}

    s_y = s.year # starting year

    while cmp(s, e) != 0:
        print s.isoformat()

        if s_y != s.year:
            s_y = s.year
            gc.collect()

        c = get_comment_list(s)
        if len(c) == 0:
            s = incrementDate(s)
            continue
        
        # insert whatever you want to do here

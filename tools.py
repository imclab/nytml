import datetime, random, json
from datetime import date

# increment date object d by one day
def incrementDate(d):
    return date.fromordinal((d.toordinal()+1))

# returns a random date between year start and year end
def randomDate(s, e):
    def f(y): return int((datetime.date(y, 1, 1)).toordinal())
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

# loads n comments from the dataset (2005 - 2013). 
# If date is unspecified then pick a random starting date. 
# If section is unspecified then load comments of any section
def load_n_comments(n, start=None, section=None):

    if start is not None: 
        start = datefromISO(start)
    else: start = randomDate(2005, 2013)

    n, end, comments = int(n), datetime.date(2014,1,1), []

    def bySection(c): return c['section'] == section

    while True:

        if cmp(start, end) == 0: return comments
        name = str(start.year) + '/' + start.isoformat() + '.json'
        
        try:
            f = open(name, 'r')
            c = json.load(f)
            f.close()
        except ValueError:
            print 'error on ' + start.isoformat()
            start = incrementDate(start)
            continue

        if section is not None: c = filter(bySection, c)
        comments.extend(c)

        c_len = len(comments)

        if c_len > n: return comments[:n]
        elif c_len == n: return comments
        else: start = incrementDate(start)
        

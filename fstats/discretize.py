import Orange, orange, numpy
from numpy import array

def show_values(data, heading):
    print heading
    for a in data.domain.attributes: 
        cutoffs = reduce(lambda x,y: x+', '+y, [i for i in a.values])
        print "%s: %s" % (a.name, cutoffs)

def main():

    data = Orange.data.Table('recs.tab')
    recs_d = Orange.feature.discretization.Entropy('recs', data)
    data2 = data.select([data.domain['recs'], recs_d], data.domain.class_var)
    for ex in data2[:10]: print ex

main()

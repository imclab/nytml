import Orange

data = Orange.data.Table('features.tab')
print 'Loaded features.tab into Orange Data Table'
entropy = Orange.feature.discretization.Entropy()
disc_data = Orange.data.discretization.DiscretizeTable(data, method=entropy)

for attr in disc_data.domain.attributes: 
    print "%s : %s" % (attr.name, attr.values)
                                                     

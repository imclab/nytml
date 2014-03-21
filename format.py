import sentiword, datetime, string, tools, json, time, sys
from urllib2 import urlopen
from datetime import date

def getSection(articleURL):
  section = None
  url = articleURL.split('.')
  try:
    section = (url[0].split('//'))[1]
    if section == 'www':
      body = (url[2].split('/'))
      if body[1] in ('restaurants', 'roomfordebate'): 
        section = body[1]
      elif body[1] in ('interactive', 'aponline', 'reuters'):
        if body[2].isdigit(): section = body[5]
        else: section = body[2]
      elif body[2] == 'magazine': section = 'magazine'
      else: section = body[4]
  except IndexError: return None
  return section

def getSentiment(txt):
  sent = {'pos':0.0,'neg':0.0}
  def f(x): return x.lower()
  exc, v = string.punctuation, txt.encode('ascii', 'ignore')
  k = (v.translate(string.maketrans("",""), exc)).split()
  tokens, i = map(f, k), 0
  for t in tokens:
    if t in wordmap:
      i += 1
      ss = wordmap[t]
      sent['pos'] += ss['pos']
      sent['neg'] += ss['neg']
    else: continue
  for j in sent:
    if i > 0: sent[j] /= i
    else: sent[j] = 0.0
  return (len(k), sent)

wordmap = sentiword.parse()

def analyze(comment):
  ne = ['status', 'sharing', 'userTitle', 'userURL', 
        'replies', 'userComments', 'email_status', 'times_people']
  for k in ne: 
    if k in comment: del comment[k]

  if 'articleURL' in comment:
    comment['section'] = getSection(comment['articleURL'])
  else: comment['section'] = None

  cb = 'commentBody'

  if cb in comment:
    if comment[cb] is not None:
      wc, sent = getSentiment(comment[cb])
      comment['wordcount'], comment['sentiment'] = wc, sent
    else: comment['sentiment'] = None
  else: comment['sentiment'] = None
    
  return comment

def clean(comment):
  flags = ['section', 'sentiment']
  for f in flags:
    if f in comment:
      if comment[f] is None: return False
    else: print comment
  return True

def main():

  s = datetime.date(2011,1,1)
  e = datetime.date(2014,1,1)

  while (tools.compareDate(s, e) != 0):

    name = str(s.year) + '/' + s.isoformat() + '.json'

    try:
      f = open(name, 'r')
      cls = json.load(f)
      f.close()
    except ValueError:
      print 'error on ' + s.isoformat()
      s = incr(s)
      continue

    cls_a = map(analyze, cls)
    cls_f = filter(clean, cls_a)

    f_new = open(name, 'w+')
    f_new.write(json.dumps(cls_f))
    f_new.close()

    s = tools.incrementDate(s)
    print s.isoformat()

main()

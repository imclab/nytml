from urllib2 import urlopen
import json
from json import loads
from json import dumps
import datetime
from datetime import date
import time
import pprint

limitError = "<class 'urllib2.HTTPError'>"

keys = [ "api-key=cd6479409e9d2849d2c8f0246ab895ea:10:68731810",
         "api-key=8c5b6144d7eb91d5acc87de2521d449b:8:58236592",
         "api-key=fc09e5a8da1f085fcb62f6bf516a4c9c:17:68705600",
         "api-key=c75a9fcf75c73f36c5607eaae90c617b:8:68729772" ]

print len(keys)

idx = 0
gkey = keys[idx]

def nextKey():
  global idx
  idx = (idx + 1) % len(keys)
  global gkey
  gkey = keys[idx]

""" creates an API request link with the given date and offset n """
def makeURL(d, n):

  """ ex: converts "2010-12-12" to "20101212" """
  date = d.replace("-","")

  f = ".json?"
  inc = "&offset=" + str(n) + "&"
  url = "http://api.nytimes.com/svc/community/v2/comments/by-date/"
  
  if (n > 0):
    link = url + date + f + inc + gkey
  else:
    link = url + date + f + gkey
  print link
  return link

""" returns a tuple with (n,l) where n is the number 
    of comments and l is the list of comments retrieved """
def makeRequest(date, offset):
    try:

      url = makeURL(date, offset)
      response = loads(urlopen(url).read())
      n = int((response['results'])['totalCommentsFound'])
      l = (response['results'])['comments']
      return (n, l)

    except Exception as inst:
      e = str(type(inst))
      if e == limitError:
        nextKey()
        print e
        print "key changed"
      else:
        print e
        print inst.args
        print inst

      time.sleep(5)
      return makeRequest(date, offset)

def retrieveComments(d):
  r = makeRequest(d, 0)
  n, comments = r[0], r[1]
  if (n <= 25):
    return comments
  else:
    i = 25
    while (i < n):
      j = makeRequest(d, i)
      comments.extend(j[1])
      i = i + 25
    return comments

def incr(d):
  return date.fromordinal((d.toordinal()+1))

# arguments are date objects
def writeComments(start, end):
  while (start.isoformat() != end.isoformat()):
    dstr = start.isoformat()
    fileName = dstr + ".json"
    myFile = open(fileName, 'w+')
    comments = retrieveComments(dstr)
    myFile.write(dumps(comments))
    myFile.close()
    start = incr(start)

myStart = datetime.date(2013,3,27)
myEnd = datetime.date(2013,3,28)
writeComments(myStart, myEnd)

#startDate = datetime.date(2005,1,1)

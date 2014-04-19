nytml
=====

Python tools and scripts to do machine learning on NYTimes comments

Data files contain a list of comment dictionaries with the following fields:

     'commentTitle' - unique string
     'display_name' - unique string
     'sentiment' : { 'pos' : P, 'neg' : N } - P and N are floats
     'section' - string, discrete variable
     'wordcount' - integer
     'commentBody' - unique string
     'commentSequence' - positive integer
     'location' - unique string
     'editorsSelection' - integer
     'approveDate' - POSIX timestamp, use datetime.datetime.fromtimestamp
     'articleURL' - unique string
     'recommendationCount' - positive integer
     

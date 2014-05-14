nytml
=====

Python tools and scripts to do machine learning on NYTimes comments

Uses the following Python modules for primary data analysis:

Orange
scikit-learn
TextBlob

Along with standard tools of numpy, scipy, and matplotlb.

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
     

#!/bin/bash
#Mami Sasaki
#Nat Byington
#Hw:Q2 batch file

#with binarizing
./binarize.py ../../dropbox/09-10/572/hw2/examples/train.vectors.txt bintrain.txt
./binarize.py ../../dropbox/09-10/572/hw2/examples/test.vectors.txt bintest.txt
info2vectors --input bintrain.txt --output bintrain.vectors
info2vectors --use-pipe-from bintrain.vectors --input bintest.txt --output bintest.vectors
vectors2classify --training-file bintrain.vectors --testing-file bintest.vectors --trainer DecisionTree >q2.stdout 2>q2.stderr

#without binarizing
info2vectors --input ../../dropbox/09-10/572/hw2/examples/train.vectors.txt --output train.vectors
info2vectors --use-pipe-from train.vectors --input ../../dropbox/09-10/572/hw2/examples/test.vectors.txt --output test.vectors
vectors2classify --training-file train.vectors --testing-file test.vectors --trainer DecisionTree >test.stdout 2>test.stderr

#compare the result
diff q2.stdout test.stdout >diff.log

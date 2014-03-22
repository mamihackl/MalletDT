#!/bin/bash
#Mami Sasaki 
#Nat Byington
#HW2:Q3 

info2vectors --input ../../dropbox/09-10/572/hw2/examples/train.vectors.txt --output train.vectors
info2vectors --use-pipe-from train.vectors --input ../../dropbox/09-10/572/hw2/examples/test.vectors.txt --output test.vectors

vectors2classify --training-file train.vectors --testing-file test.vectors --trainer "new DecisionTreeTrainer(1)" >depth1.stdout 2>depth1.stderr
vectors2classify --training-file train.vectors --testing-file test.vectors --trainer "new DecisionTreeTrainer(2)" >depth2.stdout 2>depth2.stderr
vectors2classify --training-file train.vectors --testing-file test.vectors --trainer "new DecisionTreeTrainer(4)" >depth4.stdout 2>depth4.stderr
vectors2classify --training-file train.vectors --testing-file test.vectors --trainer "new DecisionTreeTrainer(10)" >depth10.stdout 2>depth10.stderr
vectors2classify --training-file train.vectors --testing-file test.vectors --trainer "new DecisionTreeTrainer(20)" >depth20.stdout 2>depth20.stderr
vectors2classify --training-file train.vectors --testing-file test.vectors --trainer "new DecisionTreeTrainer(50)" >depth50.stdout 2>depth50.stderr
vectors2classify --training-file train.vectors --testing-file test.vectors --trainer "new DecisionTreeTrainer(100)" >depth100.stdout 2>depth100.stderr
vectors2classify --training-file train.vectors --testing-file test.vectors --trainer "new DecisionTreeTrainer(1000)" >depth1000.stdout 2>depth1000.stderr


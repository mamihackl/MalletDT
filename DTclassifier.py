#!/opt/python-2.6/bin/python2.6
# Mami Sasaki and Nat Byington
# LING 572 HW2 
# DT Classifier -- uses a DT model file to classify training and testing data,
#                  accuracy results are output to stdout. 
# Args: training file, testing file, model file, sys_out file
# "vector" data structure contains information about a specific document
# "vector" format: 3-tuple containing ("name", "class", feature_set)
 
# Imports

import sys
import re
import random
import operator

# Classes

class Node:
    leaf_node = False
    feature = False
    probs = {} # probabilities for leaf nodes
    yes_node = False
    no_node = False
    parent = '' # for debugging
    
    def __init__(self, parent):
        self.parent = parent

    def add_leaf(self, path_list, probs):
        ''' Recursively add a leaf node to a DT. '''
        if not self.feature:
            self.feature = path_list[0].strip('!')
        # base case
        if len(path_list) == 1:            
            if path_list[0].startswith('!'):
                self.no_node = Node(path_list[0])
                self.no_node.leaf_node = True
                self.no_node.probs = probs
            else:
                self.yes_node = Node(path_list[0])
                self.yes_node.leaf_node = True
                self.yes_node.probs = probs
        else:
            new_path_list = path_list[1:]
            if path_list[0].startswith('!'):
                if self.no_node:
                    self.no_node.add_leaf(new_path_list, probs)
                else:
                    self.no_node = Node(path_list[0])
                    self.no_node.add_leaf(new_path_list, probs)
            else:
                if self.yes_node:
                    self.yes_node.add_leaf(new_path_list, probs)
                else:
                    self.yes_node = Node(path_list[0])
                    self.yes_node.add_leaf(new_path_list, probs)
                
    def evaluate(self, vector):
        ''' Recursively evaluate a vector against a node. '''
        if self.feature in vector[2]:
            if self.yes_node.leaf_node:
                return self.yes_node.probs
            else:
                return self.yes_node.evaluate(vector)
        else:
            if self.no_node.leaf_node:
                return self.no_node.probs
            else:
                return self.no_node.evaluate(vector)
    
    def prnt(self):
        if self.leaf_node:
            print 'leaf!'
        else:
            print self.feature
            print 'yes for ' + self.feature
            if self.yes_node:
                self.yes_node.prnt()
            print 'no for ' + self.feature
            if self.no_node:
                self.no_node.prnt()

# Functions

def choose_highest(probs):
    ''' Take a dict containing probabilities by class and return the name
        of the class with the highest probability. '''
    sorted_list = sorted(probs.iteritems(), key=operator.itemgetter(1), reverse=True)
    if sorted_list[0][1] == sorted_list[1][1]:
        return random.choice([sorted_list[0][0], sorted_list[1][0]])
    else:
        return sorted_list[0][0]
        
    
        

# Global variables

TRAINING = open(sys.argv[1])
TESTING = open(sys.argv[2])
MODEL = open(sys.argv[3])
SYSOUT = open(sys.argv[4], 'w')

training_vectors = []
testing_vectors = []
DT_root = Node("root")
classes = set()

# Main

# extract training vectors to evaluate
for line in TRAINING.readlines():
    feature_set = set()
    instance_name = re.match(r'(^[\S]+) ([\S]+) ', line).group(1)
    class_name = re.match(r'(^[\S]+) ([\S]+) ', line).group(2)
    features = re.findall(r'([A-Za-z]+) [0-9]+', line)
    for f in features:
        feature_set.add(f)
    vector = (instance_name, class_name, feature_set)
    classes.add(class_name)
    training_vectors.append(vector)

# extract testing vectors to evaluate    
for line in TESTING.readlines():
    feature_set = set()
    instance_name = re.match(r'(^[\S]+) ([\S]+) ', line).group(1)
    class_name = re.match(r'(^[\S]+) ([\S]+) ', line).group(2)
    features = re.findall(r'([A-Za-z]+) [0-9]+', line)
    for f in features:
        feature_set.add(f)
    vector = (instance_name, class_name, feature_set)
    testing_vectors.append(vector)

# create DT by parsing model file
for line in MODEL.readlines():
    probs = {}
    path = re.match(r'(^[\S]+) [0-9]+ (.+$)', line).group(1)
    prob_part = re.match(r'(^[\S]+) [0-9]+ (.+$)', line).group(2)
    path_list = path.split('&')
    p = re.findall(r'([\S]+) ([0-1]\.[0-9]+)', prob_part)
    for i in p:
        probs[i[0]] = float(i[1])
    DT_root.add_leaf(path_list, probs)
    
# classify training data; generate sys_out; output confusion matrix
SYSOUT.write('%%%%% training data: \n')
sys.stdout.write('Confusion matrix for the training data:\n')
sys.stdout.write('row is truth, column is system output \n\n')
training_correct = 0.0

training_matrix = dict( [(x, {}) for x in classes] )
for c in classes:
    for c2 in classes:
        training_matrix[c][c2] = 0
    
for vector in training_vectors:
    probs = DT_root.evaluate(vector)
    result = choose_highest(probs)
    output = [vector[0], vector[1]]
    for class_name in probs:
        output.append(class_name)
        output.append(str(probs[class_name]))
    training_matrix[vector[1]][result] += 1
    output.append('\n')
    SYSOUT.write(' '.join(output))
    
sys.stdout.write('\t\t')
for c in classes:
    sys.stdout.write(' ' + c)
    training_correct += training_matrix[c][c]
sys.stdout.write('\n')
for c in classes:
    sys.stdout.write(c)
    for c2 in classes:
        sys.stdout.write(' ' + str(training_matrix[c][c2]))
    sys.stdout.write('\n')
print ''
print 'training accuracy = ' + str(training_correct / len(training_vectors))
print ''
print ''

    
# classify testing data; generate sys_out; output confusion matrix
SYSOUT.write('\n\n%%%%% testing data: \n')
sys.stdout.write('Confusion matrix for the training data:\n')
sys.stdout.write('row is truth, column is system output \n\n')
testing_correct = 0.0    
    
testing_matrix = dict( [(x, {}) for x in classes] )
for c in classes:
    for c2 in classes:
        testing_matrix[c][c2] = 0

for vector in testing_vectors:
    probs = DT_root.evaluate(vector)
    testing_result = choose_highest(probs)
    output = [vector[0], vector[1]]
    for class_name in probs:
        output.append(class_name)
        output.append(str(probs[class_name]))
    testing_matrix[vector[1]][testing_result] += 1
    output.append('\n')
    SYSOUT.write(' '.join(output))
    
sys.stdout.write('\t\t')
for c in classes:
    sys.stdout.write(' ' + c)
    testing_correct += testing_matrix[c][c]
sys.stdout.write('\n')
for c in classes:
    sys.stdout.write(c)
    for c2 in classes:
        sys.stdout.write(' ' + str(testing_matrix[c][c2]))
    sys.stdout.write('\n')
print ''
print 'testing accuracy = ' + str(testing_correct / len(testing_vectors))
print ''
print ''        
        


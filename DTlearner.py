#!/opt/python-2.6/bin/python2.6
# Mami Sasaki and Nat Byington
# LING 572 HW2 
# DT Learner -- creates a DT model file using recursion
# Args: training vectors, max depth, min gain, model file.
# "vector" data structure contains information about a specific document
# "vector" format: 3-tuple containing ("name", "class", feature_set)
 
# Imports

import sys
import re
import time
import math

# Functions

def calc_entropy(counts):
    ''' Take dictionary containing counts per class and return entropy.'''
    total_count = 0.0
    for c in counts:
        total_count += counts[c]
    h_neg = 0.0
    if total_count > 0:
        for c in counts:
            p_x = counts[c] / total_count
            if (p_x != 0):
                h_neg += p_x * math.log(p_x, 2)
    return (h_neg * -1)

def output_leaf(vector_list, current_path):
    ''' Write leaf node info to the model file. vector_list contains
        the vectors associated with the current leaf node, and current_path
        is the string showing the path to the current leaf node from the
        root node.'''
    # calculate probability of each class
    total_count = len(vector_list)
    class_counts = {}
    for vector in vector_list:
        increment_counter(class_counts, vector[1])
    # create output string
    output = [current_path, str(total_count)]
    for c in CLASSES:
        if c in class_counts:
            prob = class_counts[c] / float(total_count)
        else:
            prob = 0.0
        output.append(c)
        output.append(str(prob))
    output.append('\n')
    MODEL_FILE.write(' '.join(output))
        
def increment_counter(dic, key):
    ''' Takes a specially created counter dictionary and increments the value
        associated with key by 1 (or adds key with value of 1 if not there)'''
    if key in dic:
        dic[key] += 1
    else:
        dic[key] = 1
    
def create_tree(vector_list, node_entropy, current_depth, current_path, used_features):
    ''' Recursively create a decision tree based on best info gain. Each
        node either splits or becomes a leaf node that gets written to 
        the model file. used_features is a list of strings showing which
        features have already been used in the path.'''
    # check tree depth before doing any further calculations
    if (current_depth >= MAX_DEPTH):
        output_leaf(vector_list, current_path)
    else:
        # find remaining feature with best info gain
        best_feature = ['', 0.0, 0.0] #[feature, f_entropy, notf_entropy]
        best_gain = MIN_GAIN 
        node_feature_set = set()
        for vector in vector_list:
            node_feature_set.update(vector[2]) # gather all features
        for used_f in used_features:
            if used_f in node_feature_set:
                node_feature_set.remove(used_f) # remove used features
        for feature in node_feature_set:
            class_count_f = {}
            class_count_notf = {}
            total_f = 0.0
            total_notf = 0.0
            for vector in vector_list:
                if feature in vector[2]:
                    increment_counter(class_count_f, vector[1])
                    total_f += 1
                else:
                    increment_counter(class_count_notf, vector[1])
                    total_notf += 1
            f_entropy = calc_entropy(class_count_f)
            notf_entropy = calc_entropy(class_count_notf)
            total_count = total_f + total_notf
            gain = node_entropy - (((total_f/total_count)*f_entropy) 
                                   + ((total_notf/total_count)*notf_entropy))
            if (gain > best_gain):
                best_gain = gain
                best_feature = [feature, f_entropy, notf_entropy]
        # split or create leaf node
        if (best_feature[0] != ''): # if a best feature has been found
            if current_depth == 0:
                f_path = best_feature[0]
                notf_path = '!' + best_feature[0]
            else:    
                f_path = current_path + '&' + best_feature[0]
                notf_path = current_path + '&!' + best_feature[0]
            depth = current_depth + 1
            u = used_features
            u.append(best_feature[0])
            # divide vector_list according to best feature
            f_vectors = []
            notf_vectors = []
            for vector in vector_list:
                if best_feature[0] in vector[2]:
                    f_vectors.append(vector)
                else:
                    notf_vectors.append(vector)
            # split on feature by creating two new trees
            create_tree(f_vectors, best_feature[1], depth, f_path, u)
            create_tree(notf_vectors, best_feature[2], depth, notf_path, u)
        else:
            output_leaf(vector_list, current_path)
                    
       
    
    
    
# Global variables

TRAINING = open(sys.argv[1])
MAX_DEPTH = int(sys.argv[2])
MIN_GAIN = float(sys.argv[3])
MODEL_FILE = open(sys.argv[4], 'w')
CLASSES = {} # a dict containing a count for each class
    
# Main

sys.stderr.write("start time: " + time.ctime() + '\n')

# convert training file into vector list, grab initial entropy
vector_list = []

for line in TRAINING.readlines():
    feature_set = set()
    instance_name = re.match(r'(^[\S]+) ([\S]+) ', line).group(1)
    class_name = re.match(r'(^[\S]+) ([\S]+) ', line).group(2)
    increment_counter(CLASSES, class_name)
    features = re.findall(r'([A-Za-z]+) [0-9]+', line)
    for f in features:
        feature_set.add(f)
    vector = (instance_name, class_name, feature_set)
    vector_list.append(vector)
initial_entropy = calc_entropy(CLASSES)

# create the root decision tree 

create_tree(vector_list, initial_entropy, 0, '', [])

sys.stderr.write("end time: " + time.ctime() + '\n')

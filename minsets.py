import sys
import os
import re
import ast
import math
import random

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def inter(list1,list2): #intersection of two list
    intersect = [a for a in list1 if a in list2]
    return intersect

def compatible(split1,split2):
    checker = [0,0,0,0]
    if len(inter(split1[0],split2[0])) > 0:
        checker[0] = 1
    if len(inter(split1[1],split2[0])) > 0:
        checker[1] = 1
    if len(inter(split1[0],split2[1])) > 0:
        checker[2] = 1
    if len(inter(split1[1],split2[1])) > 0:
        checker[3] = 1
    if sum(checker) == 0 or sum(checker) == 1:
        return "ERROR"
    if sum(checker) == 2:
        return "SAME"
    if sum(checker) == 3:
        return True
    if sum(checker) == 4:
        return False

def list_complement(X,sub_list):
    return [element for element in X if element not in sub_list]

firstfile = input("What is the first filename? ")
with open(firstfile, "r") as f:
	first_list = f.read().splitlines()
    
cleaned_split_list = []    
    
for long_name in first_list:
    nw_splits = re.sub("\[.+\] \\t ", "", long_name)
    nw_splits = re.sub(",", "", nw_splits)
    nw_splits = re.sub("\s", ",", nw_splits)
    nw_splits = "["+nw_splits+"]"
    nw_splits = ast.literal_eval(nw_splits)
    cleaned_split_list.append(nw_splits)


n = int(input("What is n? "))
X = range(1,n+1)

split_list = [(a,list_complement(X,a)) for a in cleaned_split_list]

minimum_value = 2*math.factorial(n)
iterations = 1000
for i in range(iterations):

    list_of_trees = []
    
    random.shuffle(split_list)

    for split in split_list:
        if len(list_of_trees) == 0:
            list_of_trees.append([split])
        else:
            found_one = False
            for tree in list_of_trees:
                compat_checker = True
                for tree_split in tree:
                    if compatible(split,tree_split) != True:
                        compat_checker = False
                if compat_checker == True:
                    tree.append(split)
                    found_one = True
                    break 
            if found_one == False:
                list_of_trees.append([split])
    x = len(list_of_trees)
    if x < minimum_value:
        minimum_value = x
    sys.stdout.write("\rCalculating iteration %i of %i . That's %f %%" % (i+1,iterations, (i+1)/iterations *100))
    sys.stdout.flush()

print("\nShortest was ",minimum_value)

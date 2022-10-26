import sys
sys.path.append("../misc/metrics")

import numpy as np
import pandas as pd
from classification_metrics import compute_recall, compute_precision, compute_f1_score
from decisionTree import Node
from copy import deepcopy

def randomForest(X, y, forest_size=50, measure="Entropy", max_depth=None, randomSeed=None, samples_to_split=None, max_features="sqrt", tree_size=1.0, weights_initialization=list()):
    if randomSeed!=None:
        np.random.seed(randomSeed)
    if max_features=="sqrt":
        tree_max_features = int(np.sqrt(X.shape[1]))
    elif max_features=="log":
        tree_max_features = int(np.log(X.shape[1]))
    elif isinstance(max_features, int):
        if max_features>X.shape[1] or max_features<=0:
            print(f"Number of features per tree given as an int ({max_features}) can't exceed total number of features ({X.shape[1]}) and can't be below 1")
            return
        else:
            tree_max_features = max_features
    elif isinstance(max_features, float):
        if max_features<=0 or max_features>1:
            print(f"Number of features per tree given as a float must be in interval (0, 1]. Recieved {max_features}")
            return
        else:
            tree_max_features = int(max_features*X.shape[1])
    else:
        print(f"max_feature argument not understood. Recieved {max_features}")
        return 
    if isinstance(tree_size, float):
        if tree_size>0 and tree_size<=1.0:
            tree_sample_size = int(X.shape[0]*tree_size)
        else:
            print(f"Tree size must be a float between 0.0 and 1.0, recieved {tree_size} of type {type(tree_size)}")
            return
    else:
        print(f"Tree size must be a float between 0.0 and 1.0, recived {tree_size} of type {type(tree_size)}")
        return
    if not isinstance(weights_initialization, list):
        print(f"Weights initialization must be a list, recieved {type(weights_initialization)}")
        return
    else:
        if len(weights_initialization)!=forest_size and len(weights_initialization)!=0:
            print(f"Weights initialization must be a list of length equal to forest size. recieved weights initialization of length {len(weights_initialization)} and forest of size {forest_size}")
            return
        if len(weights_initialization)==0:
            weights_initialization = np.ones(forest_size)

    trees = list()
    for i in range(0, forest_size):
        this_tree_feature_list = list()
        while(len(this_tree_feature_list)<tree_max_features):
            this_feature = np.random.randint(0, X.shape[1])
            if this_feature not in this_tree_feature_list:
                this_tree_feature_list.append(this_feature)
        chosen_samples = np.random.randint(0, X.shape[0], size=tree_sample_size)
        inter = np.concatenate((X, y.reshape(-1, 1)), axis=1)
        this_tree_dataset_X = deepcopy(inter[chosen_samples,:][:,this_tree_feature_list])
        this_tree_dataset_y = deepcopy(inter[chosen_samples,:][:, -1])
        this_tree = Node(this_tree_dataset_X, this_tree_dataset_y, measure=measure, max_depth=max_depth, randomSeed=randomSeed, samples_to_split=samples_to_split)
        this_tree.expand()
        trees.append((this_tree, weights_initialization[i]))
    return trees

def randomForestPredict(randomForest, X):
    sum_weights = 0
    sum_votes = np.zeros(X.shape[0])
    for tree in randomForest:
        this_tree = tree[0]
        this_tree.printInfo()
        this_weight = tree[1]
        sum_weights += this_weight
        sum_votes += this_weight * this_tree.predict(X)
    sum_votes = sum_votes/sum_weights
    sum_votes[sum_votes>=0.5] = 1
    sum_votes[sum_votes<0.5] = 0
    return sum_votes

if __name__=="__main__":
    """
    First, load the dataset and prepare the data by transforming quality in numerical data. 
    Also split the dataset in 66:33 for training:testing
    """
    dataset = pd.read_csv("../misc/datasets/wine.csv")
    for i in range(0, dataset.shape[0]):
        if dataset.iloc[i,-1]=="good":
            dataset.iloc[i,-1]=1
        else:
            dataset.iloc[i,-1]=0

    X = np.asarray(dataset)[:, :-1]
    y = np.asarray(dataset)[:, -1]
    split = int(X.shape[0]*(66/100))

    X_train = X[:split]
    y_train = y[:split]
    X_test = X[split:]
    y_test = y[split:]

    print(f"There are {X_train.shape[0]} data for training and {X_test.shape[0]} data for testing")
    print(f"There are {X_train.shape[1]} features in each")

    """
    Single decision tree performance
    """
    print("Single decision tree performance:")
    decisionTree = Node(X_train, y_train)
    decisionTree.expand()
    y_pred = decisionTree.predict(X_test)
    precision = compute_precision(y_test, y_pred)
    recall = compute_recall(y_test, y_pred)
    f1 = compute_f1_score(y_test, y_pred)
    print(f"Precision: {precision}\nRecall: {recall}\nf1-score: {f1}")
    print("-"*60)

    """
    Random forest performance
    """
    print("Random forest performance")
    randomForest_classifier = randomForest(X_train, y_train)
    y_pred = randomForestPredict(randomForest_classifier, X_test)
    precision = compute_precision(y_test, y_pred)
    recall = compute_recall(y_test, y_pred)
    f1 = compute_f1_score(y_test, y_pred)
    print(f"Precision: {precision}\nRecall: {recall}\nf1-score: {f1}")
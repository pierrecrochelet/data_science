import sys
sys.path.append("../misc/metrics")

import numpy as np
import pandas as pd
from classification_metrics import compute_recall, compute_precision, compute_f1_score

"""
Define the decision tree as nodes that can have up to two children. This decision tree works for both numerical and categorical features at the same time.
"""
class Node:

    """
    Initialize the node with the data. To consider both categorical and numerical data, the data type is logged in self.featureTypes, which is induced from the data if not provided.
    The node is a leaf node if all of its data belongs to the same class. The prediction Value of the node is the class for which the node has most data.
    The node has two children: left and right. 
    The featureSplit and featureSplitThreshold attributes are calculated in the findSplit function and represent the best feature and value to split this node.
    """
    def __init__(self, X, y, featureTypes=None, depth=0, max_depth=None, randomSeed=None, samples_to_split=None):
        self.X = X
        self.y = y
        if featureTypes==None:
            self.featureTypes = []
            for i in range(0, X.shape[1]):
                self.featureTypes.append("Categorical" if isinstance(X[0,i], str) else "Numerical")
        else:
            self.featureTypes = featureTypes
        ones = np.argwhere(y==1).shape[0]
        zeros = y.shape[0]-ones
        if ones>zeros:
            self.predictionValue = 1
        else:
            self.predictionValue = 0
        if ones==0 or zeros==0:
            self.entropy=0
        else:
            self.entropy = -( ((ones/y.shape[0])*np.log2(ones/y.shape[0])) + ((zeros/y.shape[0])*np.log2(zeros/y.shape[0])) )
        self.left = None
        self.right = None
        self.featureSplit = None
        self.featureSplitThreshold = None
        self.depth = depth
        self.maxDepth = max_depth
        self.SubtreeDepth = 1
        if randomSeed!=None:
            np.random.seed(randomSeed)
        if samples_to_split!=None:
            if samples_to_split>0 and samples_to_split<1:
                self.samplesToSplit = int(samples_to_split*X.shape[0])
            else:
                self.samplesToSplit = int(samples_to_split)
        else:
            self.samplesToSplit=None
        if ones==y.shape[0] or ones==0 or (max_depth!=None and depth>=max_depth) or (self.samplesToSplit!=None and self.samplesToSplit>X.shape[0]):
            self.leaf=True
        else:
            self.leaf=False

    """
    Loops through all features and all values (or threshold values) in the data to find the best split. 
    The threshold values for numerical features are calculating by sorting all unique values and then taking the average of each pair.
    """
    def findSplit(self):

        chosen = []
        best_information_gain = 0

        for i in range(0, self.X.shape[1]):

            values = np.unique(self.X[:,i])

            if self.featureTypes[i]=="Categorical":
                for value in values:

                    # Calculate entropy in each split
                    ones = np.argwhere(self.y[self.X[:,i]==value]==1).shape[0]
                    zeros = self.y[self.X[:,i]==values].shape[0]-ones
                    if ones==0 or zeros==0:
                        entropy1 = 0
                    else:
                        ones = ones/self.y[self.X[:,i]==values].shape[0]
                        zeros = zeros/self.y[self.X[:,i]==values].shape[0]
                        entropy1 = (-( ones*np.log2(ones) + zeros*np.log2(zeros) )) * (self.y[self.X[:,i]==values].shape[0]/self.y.shape[0])

                    ones = np.argwhere(self.y[self.X[:,i]!=value]==1).shape[0]
                    zeros = self.y[self.X[:,i]!=values].shape[0]-ones
                    if ones==0 or zeros==0:
                        entropy2 = 0
                    else:
                        ones = ones/self.y[self.X[:,i]!=values].shape[0]
                        zeros = zeros/self.y[self.X[:,i]!=values].shape[0]
                        entropy2 = -( ones*np.log2(ones) + zeros*np.log2(zeros) ) * (self.y[self.X[:,i]!=values].shape[0]/self.y.shape[0])
                        
                    # Calculate information gain
                    information_gain = self.entropy-(entropy1+entropy2)

                    # Update best information gain and returned value.
                    if information_gain>best_information_gain:
                        best_information_gain = information_gain
                        chosen = [(i, value)]
                    if information_gain==best_information_gain:
                        chosen.append((i, value))

            else:
                for j in range(1, len(values)):
                    threshold = values[j-1] + ((values[j]-values[j-1])/2)

                    # Calculate entropy in each split
                    ones = np.argwhere(self.y[self.X[:,i]>threshold]==1).shape[0]
                    zeros = self.y[self.X[:,i]>threshold].shape[0]-ones
                    if ones==0 or zeros==0:
                        entropy1 = 0
                    else:
                        ones = ones/self.y[self.X[:,i]>threshold].shape[0]
                        zeros = zeros/self.y[self.X[:,i]>threshold].shape[0]
                        entropy1 = (-( ones*np.log2(ones) + zeros*np.log2(zeros) )) * (self.y[self.X[:,i]>threshold].shape[0]/self.y.shape[0])

                    ones = np.argwhere(self.y[self.X[:,i]<threshold]==1).shape[0]
                    zeros = self.y[self.X[:,i]<threshold].shape[0]-ones
                    if ones==0 or zeros==0:
                        entropy2 = 0
                    else:
                        ones = ones/self.y[self.X[:,i]<threshold].shape[0]
                        zeros = zeros/self.y[self.X[:,i]<threshold].shape[0]
                        entropy2 = (-( ones*np.log2(ones) + zeros*np.log2(zeros) )) * (self.y[self.X[:,i]<threshold].shape[0]/self.y.shape[0])

                    # Calculate information gain
                    information_gain = self.entropy-(entropy1+entropy2)
                    
                    # Update best information gain and returned value
                    if information_gain>best_information_gain:
                        best_information_gain = information_gain
                        chosen = [(i, threshold)]
                    if information_gain==best_information_gain:
                        chosen.append((i, threshold))
        try:
            chosen = chosen[np.random.randint(len(chosen))]
        except ValueError:
            print(chosen)
            print(self.X)
            print(self.y)
            print(self.leaf)
            exit(0)
        self.featureSplit = chosen[0]
        self.featureSplitThreshold = chosen[1]

    """
    Expand the whole tree to fit on the given data by recursively calling this function in the children nodes created and making the split according to the results returned by findSplit.
    """
    def expand(self):
        # Only expand if this node is not a leaf node
        if self.leaf==False:

            self.findSplit()

            if self.featureTypes[self.featureSplit] == "Categorical":
                X_newLeft = self.X[self.X[:,self.featureSplit]==self.featureSplitThreshold]
                y_newLeft = self.y[self.X[:,self.featureSplit]==self.featureSplitThreshold]
                X_newRight = self.X[self.X[:,self.featureSplit]!=self.featureSplitThreshold]
                y_newRight = self.y[self.X[:,self.featureSplit]!=self.featureSplitThreshold]
            else:
                X_newLeft = self.X[self.X[:,self.featureSplit]<self.featureSplitThreshold]
                y_newLeft = self.y[self.X[:,self.featureSplit]<self.featureSplitThreshold]
                X_newRight = self.X[self.X[:,self.featureSplit]>self.featureSplitThreshold]
                y_newRight = self.y[self.X[:,self.featureSplit]>self.featureSplitThreshold]

            nodeLeft = Node(X=X_newLeft, y=y_newLeft, featureTypes=self.featureTypes, depth=self.depth+1, max_depth=self.maxDepth, samples_to_split=self.samplesToSplit)
            self.left = nodeLeft
            depthTreeLeft = nodeLeft.expand()

            nodeRight = Node(X=X_newRight, y=y_newRight, featureTypes=self.featureTypes, depth=self.depth+1, max_depth=self.maxDepth, samples_to_split=self.samplesToSplit)
            self.right = nodeRight
            depthTreeRight = nodeRight.expand()

            self.SubtreeDepth = max(depthTreeLeft, depthTreeRight)
        return self.SubtreeDepth + 1

    """
    Goes through the tree to find the leaf giving the prediction for this value
    """
    def predict_value(self, value):

        if self.leaf:
            return self.predictionValue
        else:
            if self.featureTypes[self.featureSplit] == "Categorical":
                if value[self.featureSplit]==self.featureSplitThreshold:
                    return self.left.predict_value(value)
                else:
                    return self.right.predict_value(value)
            else:
                if value[self.featureSplit]<self.featureSplitThreshold:
                    return self.left.predict_value(value)
                else:
                    return self.right.predict_value(value)

    """
    Iterate over all given values using the predict_value function to return all predictions at once in an array.
    """
    def predict(self, to_predict):

        predictions = np.zeros(to_predict.shape[0])
        for i in range(0, to_predict.shape[0]):
            predictions[i] = self.predict_value(to_predict[i])
        return predictions

    """
    Prints some information on the tree such as the max depth
    """
    def printInfo(self):
        print(f"The tree has a depth of {self.SubtreeDepth}.")

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

    decisionTree = Node(X_train, y_train)
    decisionTree.expand()
    y_pred = decisionTree.predict(X_test)
    decisionTree.printInfo()
    
    precision = compute_precision(y_test, y_pred)
    recall = compute_recall(y_test, y_pred)
    f1 = compute_f1_score(y_test, y_pred)
    print(f"Precision: {precision}\nRecall: {recall}\nf1-score: {f1}")
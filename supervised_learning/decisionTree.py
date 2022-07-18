import sys
sys.path.append("../misc/metrics")

import numpy as np
import pandas as pd
from classification_metrics import compute_recall, compute_precision, compute_f1_score

"""
Find the best value to create a split in the tree.
This will differ based on the type of the value considered.
If the value is categorical, then loop on all the categorical values and calculate information gain then return the value which maximizes the information gain.
If the value is numercial, ...
"""

def findSplit(X, y, dataType):
    for i in range(0, X.shape[0]):

        chosen = None
        best_information_gain = 0

        if dataType=="Categorical":

            # Calculate base entropy
            ones = np.argwhere(y==1).shape[0]
            zeros = y.shape[0]-ones
            base_entropy = -( ones*np.log2(ones) + zeros*np.log2(zeros) )
            values = np.unique(X)
            
            # Loop over all values
            for value in values:

                # Calculate entropy in each split
                ones = np.argwhere(y[X[i]==value]==1).shape[0]
                zeros = y[X==values].shape[0]-ones
                entropy1 = (-( ones*np.log2(ones) + zeros*np.log2(zeros) )) * (y[X==values].shape[0]/y.shape[0])
                ones = np.argwhere(y[X!=value]==1).shape[0]
                zeros = y[X!=values].shape[0]-ones
                entropy2 = -( ones*np.log2(ones) + zeros*np.log2(zeros) ) * (y[X!=values].shape[0]/y.shape[0])

                # Calculate information gain
                information_gain = base_entropy-(entropy1+entropy2)

                # Update best information gain and returned value.
                if information_gain>best_information_gain:
                    best_information_gain = information_gain
                    chosen = (i, value)
        else:

            # Calculate base entropy
            ones = np.argwhere(y==1).shape[0]
            zeros = y.shape[0]-ones
            base_entropy = -( ones*np.log2(ones) + zeros*np.log2(zeros) )
            values = np.unique(X)

            # Loop over threshold values
            diff_vals = np.unique(X)
            for j in range(1, len(diff_vals)):
                threshold = (diff_vals[j]-diff_vals[j-1])/2

                # Calculate entropy in each split
                ones = np.argwhere(y[X>threshold]==1).shape[0]
                zeros = y[X>threshold].shape[0]-ones
                entropy1 = (-( ones*np.log2(ones) + zeros*np.log2(zeros) )) * (y[X>threshold].shape[0]/y.shape[0])
                ones = np.argwhere(y[X<threshold]==1).shape[0]
                zeros = y[X<threshold].shape[0]-ones
                entropy1 = (-( ones*np.log2(ones) + zeros*np.log2(zeros) )) * (y[X<threshold].shape[0]/y.shape[0])

                # Calculate information gain
                information_gain = base_entropy-(entropy1+entropy2)
                
                # Update best information gain and returned value
                if information_gain>best_information_gain:
                    best_information_gain = information_gain
                    chosen = (i, value)
    
    return chosen

"""
Define the decision tree as nodes that can have up to two children.
"""
class Node:

    """
    Initialize the node with the data. To consider both categorical and numerical data, the data type is logged in self.featureTypes, which is induced from the data if not provided.
    The node is a leaf node if all of its data belongs to the same class. The prediction Value of the node is the class for which the node has most data.
    The node has two children: left and right. 
    The featureSplit and featureSplitThreshold attributes are calculated in the findSplit function and represent the best feature and value to split this node.
    """
    def __init__(self, X, y, featureTypes=None):
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
        if ones==y.shape[0] or ones==0:
            self.leaf=True
        else:
            self.leaf=False
        if ones>zeros:
            self.predictionValue = 1
        else:
            self.predictionValue = 0
        ones = ones/y.shape[0]
        zeros = zeros/y.shape[0]
        if ones==0 or zeros==0:
            self.entropy=0
        else:
            self.entropy = -( (ones*np.log2(ones)) + (zeros*np.log2(zeros)) )
        self.left = None
        self.right = None
        self.featureSplit = None
        self.featureSplitThreshold = None

    """
    Loops through all features and all values (or threshold values) in the data to find the best split. 
    The threshold values for numerical features are calculating by sorting all unique values and then taking the average of each pair.
    """
    def findSplit(self):

        chosen = None
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
                        chosen = (i, value)
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
                        chosen = (i, threshold)

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

            node1 = Node(X_newLeft, y_newLeft, self.featureTypes)
            self.left = node1
            node1.expand()

            node2 = Node(X_newRight, y_newRight, self.featureTypes)
            self.right = node2
            node2.expand()

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
    test = ["test"]*X.shape[0]
    X = np.concatenate((X, np.array(test).reshape(-1, 1)), axis=1)
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

    precision = compute_precision(y_test, y_pred)
    recall = compute_recall(y_test, y_pred)
    f1 = compute_f1_score(y_test, y_pred)
    print(f"Precision: {precision}\nRecall: {recall}\nf1-score: {f1}")
import sys
sys.path.append("../misc/scalers")
sys.path.append("../misc/metrics")

import numpy as np
import pandas as pd
import normal_scaler
from copy import deepcopy
from classification_metrics import compute_recall, compute_precision, compute_f1_score

"""
Define cost function used where C is the penalty of a wrongly classified term. Bigger C makes it hard-margin and lower C makes soft-margin. 
Hard margin tries to absolutely have no error making the space between the support vector smaller. As a result it will usualize perform worse when generalizing.
Soft margin accepts errors to some extent (as defined with the value C) and finds a compromise between having a low number of errors and a big space between the support vectors. 
As a result it will usually perform better when generalyzing
The first term is a measure of the margin.
We want here to maximize the distance from a point to the margin which is given by dist_a/||w|| where dist_a is the distance of point a given by |<w,a>+b|.
Rescaling elements yields max |1|/||w||. Here, maximizing 1/||w|| is the same as minimizing ||w||^2 = np.dot(W,W)
The second term is the errors of prediction weighted by the parameter C. 
In the array errors, the negative terms mean that the prediction is correct. Therefore, only errors>0 is considered in the loss function.
Also, W[0] is the intercept, usually called b in the equations.
"""

def cost_function(W, X, y, C=1):
    n_obs = X.shape[0]
    first_term = (1/2)*np.dot(W,W)
    errors = 1-(y*(np.dot(X,W[1:])+W[0]))
    second_term = (C/n_obs)*np.sum(errors[errors>0])
    return first_term+second_term

"""
Here we compute the gradien with respect to w of the loss function defined previously. 
This happens to be only W for terms correctly predicted and W-(C*y[i]*x[i]) if i was wrongly predicted.
for the intercept x[i] will always be 1 so no need to consider it in the multiplication.
"""

def cost_gradient(W, X, y, C):
    n_obs = X.shape[0]
    errors = 1-(y*(np.dot(X,W[1:])+W[0]))
    dw = np.zeros(W.shape[0])
    counter = -1
    for error in errors:
        counter+=1
        if error<0:
            dw = dw + W
        else:
            dw[1:] = dw[1:] + (W[1:] - (C*y[counter]*X[counter]))
            dw[0] = dw[0] + W[0] - (C*y[counter])
    dw = dw / n_obs
    return dw

"""
Here we compute the gradient descent which is the training of the model. First x_train and y_train are declared and we add the intercept to x_train. 
They are declare as new arrays because they are shuffled later. They are shuffled so that each iteration of the gradient descent is different in that data is passed in a different order.
The weights are initialized at random between 0 and 1, another possibility is to initialize them to be 0.
In each iteration, we go through the whole data in batches and update the weights according to the gradient of the cost function.
After each data is passed we check if this iteration has decreased the cost. If the cost wasn't decreased enough, the algorithm is stopped there.
"""

def gradient_descent(X, y, batch_size=1, epochs=100, learning_rate=0.0001, C=5, cost_threshold=0.001):
    x_train = deepcopy(X)
    y_train = deepcopy(y)
    weights = np.random.rand(x_train.shape[1]+1)
    #weights = np.zeros(x_train.shape[1]+1)
    prev_cost = float("inf")
    for _ in range(0, epochs):

        # Shuffle the arrays to get different subsets each iterations, usefull when batch_size>1
        inter = np.concatenate((x_train, y_train.reshape(-1, 1)), axis=1)
        np.random.shuffle(inter)
        x_train = inter[:,:-1]
        y_train = inter[:,-1]
        for i in range(0, x_train.shape[0], batch_size):
            # Update weights according to gradient of cost function
            dw = cost_gradient(weights, x_train[i:i+batch_size], y_train[i:i+batch_size], C)
            weights = weights - (learning_rate * dw)
        
        # Early stopping criterion if the value of the cost function doesn't change much. Can be prevented by setting cost_threshold=0
        cost = cost_function(weights, x_train, y_train, C)
        if np.abs(cost-prev_cost) < cost_threshold * prev_cost:
            return weights
        else:
            prev_cost = cost
    
    return weights

"""
Here the function predicts the label for the x values given using the weights given (calculated using the gradient_descent function).
the numpy.sign function returns 0 for the values equal to 0 so we add predicted==0 which returns 1 for the values equal to 0.
"""

def predict_values(W, X):
    predicted = np.dot(X, W[1:])+W[0]
    return np.sign(predicted)+(predicted==0)

"""
Test the implementation. I am not interested in finding the best SVM classifier here, just in implementing an SVM classifier. 
Therefore the results could be better if one was interested in playing with the parameters.
"""

if __name__=="__main__":

    """
    First, load the dataset and prepare the data by transforming quality in numerical data. 
    For SVM, it is easier if the labels are -1 and 1 instead of 0 and 1.
    Also split the dataset in 66:33 for training:testing
    """

    dataset = pd.read_csv("../misc/datasets/wine.csv")
    for i in range(0, dataset.shape[0]):
        if dataset.iloc[i,-1]=="good":
            dataset.iloc[i,-1]=1
        else:
            dataset.iloc[i,-1]=-1

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
    Scale data with custom made normal scaler
    """

    params = normal_scaler.find_parameters(X_train)
    normal_scaler.scale_data(X_train, params)

    weights = gradient_descent(X_train, y_train)
    y_pred = predict_values(weights, X_test)
    print(y_test, y_pred)
    precision = compute_precision(y_test, y_pred, true_val = 1, false_val = -1)
    recall = compute_recall(y_test, y_pred, true_val = 1, false_val = -1)
    f1 = compute_f1_score(y_test, y_pred, true_val = 1, false_val = -1)
    print(f"Precision: {precision}\nRecall: {recall}\nf1-score: {f1}")
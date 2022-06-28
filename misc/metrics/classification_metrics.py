import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

"""
Compute the 4 elements that serve as basis for every other metric, which are:
   true positives (Tp) - positive samples that are predicted as positives
   true negatives (Tn) - negative samples that are predicted as negatives
   false positives (Fp) - negative samples that are predicted as positives
   false negatives (Fn) - positive samples that are predicted as negatives
"""
def compute_basics(true, predicted):
    if true.shape[0]!=predicted.shape[0]:
        print(f"True and predicted must have same length but found {true.shape[0]} and {predicted.shape[0]}")
        return
    added = true+predicted
    subtracted = true-predicted
    Tp = np.argwhere(added==2).shape[0]
    Tn = np.argwhere(added==0).shape[0]
    Fp = np.argwhere(subtracted==-1).shape[0]
    Fn = np.argwhere(subtracted==1).shape[0]
    return Tp, Tn, Fp, Fn

"""
Displays the confusion matrix. True and predicted must be 1d arrays
"""
def confusion_matrix(true, predicted):
    Tp, Tn, Fp, Fn = compute_basics(true, predicted)
    
    matrix = np.array([[Tp, Fn], [Fp, Tn]])
    _, ax = plt.subplots()
    colormap = sns.color_palette("Blues", as_cmap=True)
    sns.heatmap(matrix, ax=ax, cmap=colormap, annot=True)
    ax.set_title("Confusion matrix")
    ax.set_xlabel("Predicted values")
    ax.set_ylabel("True values")
    ax.xaxis.set_ticklabels(['1','0'])
    ax.yaxis.set_ticklabels(['1','0'])
    plt.show()

"""
Returns the false positive rate (a.k.a. type 1 error). True and predicted must be 1d arrays
This is calculated as the number of false positives (Fp) on the number of total negatives (Fp+Tn).
In other words, it measures, out of all negatives, how many the model has incorrectly identified as positives.
"""
def false_positive_rate(true, predicted):
    _, Tn, Fp, _ = compute_basics(true, predicted)
    return (Fp/(Fp+Tn))

"""
Returns the false negative rate (a.k.a. type 2 error). True and predicted must be 1d arrays
This is calculated as the number of false negatives (Fn) on the number of total positives (Tp+Fn)
In other words, it measures, out of all positives, how many the model has incorrectly identified as negatives.
"""
def false_negative_rate(true, predicted):
    Tp, _, _, Fn = compute_basics(true, predicted)
    return (Fn/(Tp+Fn))

"""
Returns the true negative rate (a.k.a. specificity). True and predicted must be 1d arrays
This is calculated as the number of true negatives (Tn) on the number of total positives (Tp+Fn).
In other words, it measures, out of all negatives, how many the model has correctly identified as negatives.
"""
def true_negative_rate(true, predicted):
    _, Tn, Fp, _ = compute_basics(true, predicted)
    return (Tn/(Fp+Tn))

"""
Returns the negative predicted value (a.k.a. precision for negative class). True and predicted must be 1d arrays
This is calculated as the number of true negatives (Tn) on the number of all predicted negatives (Tn+Fn).
In other words, it measures, out of all negative predictions, how many were actually negatives.
"""
def negative_predicted_value(true, predicted):
    _, Tn, _, Fn = compute_basics(true, predicted)
    return (Tn/(Fn+Tn))

"""
Returns the false discovery rate. True and predicted must be 1d arrays
This is calculated as the number of false positives (Fp) on the number of all predicted positives (Fp+Tp).
In other words, it measures, out of all positive predictions, how many mistakes there are.
"""
def false_discovery_rate(true, predicted):
    Tp, _, Fp, _ = compute_basics(true, predicted)
    return (Fp/(Tp+Fp))

"""
Returns the recall (a.k.a. true positive rate, a.k.a. sensitivity). True and predicted must be 1d arrays
This is calculated as the number of true positives (Tp) on the number of all positives (Tp+Fn).
In other words, it measures, out of all positives, how many were found by the model.
"""
def recall(true, predicted):
    Tp, _, _, Fn = compute_basics(true, predicted)
    return (Tp/(Tp+Fn))

"""
Returns the precision (a.k.a. positive predicted value). True and predicted must be 1d arrays
This is calculated as the number of true positives (Tp) on the number of all predicted positives (Tp+Fp).
In other words, it measures, out of all predicted positives, how many actually positives.
"""
def precision(true, predicted):
    Tp, _, Fp, _ = compute_basics(true, predicted)
    return (Tp/(Tp+Fp))

"""
Returns the accuracy. True and predicted must be 1d arrays
This is calculated as the number of true positives (Tp) and true negatives (Tn) on the number of all observations (Tp+Tn+Fn+Fp).
In other words, it measures, out of all samples, how many correctly classified.
"""
def accuracy(true, predicted):
    Tp, Tn, Fp, Fn = compute_basics(true, predicted)
    return ((Tp+Tn)/(Tp+Tn+Fp+Fn))

"""
Returns the f1-score. True and predicted must be 1d arrays
This is calculated as precision times recall on precision added to recall.
In other words, it is a harmonic mean between precision and recall, giving both the same importance.
"""
def f1_score(true, predicted):
    Tp, _, Fp, Fn = compute_basics(true, predicted)
    return ((2*Tp)/(2*Tp+Fp+Fn))

"""
Returns the f_beta score. True and predicted must be 1d arrays
This is a generalization of the f1 score. Here, the more you care about the recall over the precision, the higher beta should be.
"""
def fBeta_score(true, predicted, beta):
    Tp, _, Fp, Fn = compute_basics(true, predicted)
    return ((Tp*(1+beta^2))/((Tp*(1+beta^2))+((beta^2)*Fn)+Fp))


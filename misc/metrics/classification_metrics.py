import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import decimal

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
Gives to option to plot it in a given axis.
"""
def confusion_matrix2(true, predicted, ax=None):
    Tp, Tn, Fp, Fn = compute_basics(true, predicted)
    
    matrix = np.array([[Tp, Fn], [Fp, Tn]])
    if ax==None:
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

"""
Returns the kappa statistic. True and predicted must be 1d arrays
This is calculated using observed_accuracy (the accuracy of the classifier) and expected accuracy (how well would a randoom classifier do looking at the confusion matrix). 
The latter is calculated looking at a percentage of time classifiers agree.
In other words, the kappa statistics measures how much better the classifier is than a random classifier. 
"""
def kappa_statistics(true, predicted):
    Tp, Tn, Fp, Fn = compute_basics(true, predicted)
    print(Tp, Tn, Fp, Fn)
    observed_accuracy = (Tp+Tn)/(Tp+Tn+Fp+Fn)
    expected_proportion_ground_positive = (Tp+Fn)/(Tp+Tn+Fp+Fn)
    expected_proportion_classifier_positive = (Tp+Fp)/(Tp+Tn+Fp+Fn)
    expected_proportion_ground_negative = (Fp+Tn)/(Tp+Tn+Fp+Fn)
    expected_proportion_classifier_negative = (Fn+Tn)/(Tp+Tn+Fp+Fn)
    expected_accuracy = (expected_proportion_ground_positive*expected_proportion_classifier_positive)+(expected_proportion_ground_negative*expected_proportion_classifier_negative)
    print(observed_accuracy, expected_accuracy)
    return (observed_accuracy-expected_accuracy)/(1 - expected_accuracy)

"""
Returns Matthews correlation coefficient (a.k.a. MCC). True and predicted must be 1d arrays
This is calculated using true and false positives and negatives and is a balanced measure. 
It returns a number between -1 and 1, with -1 being total disagreement between prediction and ground truth and +1 being a perfect prediction. 
O is also regarded as a random prediction
"""
def matthews_correlation_coefficient(true, predicted):
    Tp, Tn, Fp, Fn = compute_basics(true, predicted)
    numerator = (Tp*Tn)-Fp*Fn
    denominator = np.sqrt((Tp+Fp)*(Tp+Fn)*(Tn+Fp)*(Tn+Fn))
    return numerator/denominator

"""
Displays the receiver operating characteristic curve (a.k.a ROC curve). True and predicted must be 1d arrays
Roc is usually used to find the prediction boundary and therefore is better when used with continuous values, not with binary values as the other metrics.
Gives the option to plot it in a given axis with given label. Also, provides the degree of precision of the curve given as the number of points plotted
"""
def roc_curve(true, predicted, ax=None, label="classifier", precision=10000):
    if true.shape[0]!=predicted.shape[0]:
        print(f"True and predicted must have same length but found {true.shape[0]} and {predicted.shape[0]}")
        return
    precision = int(precision)
    if ax==None:
        _, ax = plt.subplots()
    baseline = np.linspace(0, 1, precision)
    ax.plot(baseline, baseline, '--b', label="baseline")
    FPR = np.zeros(precision)
    TPR = np.zeros(precision)
    for i in range(1, len(baseline)-1):
        new_predicted = np.zeros(predicted.shape)
        new_predicted[np.argwhere(predicted>baseline[i])] = 1
        TPR[i] = recall(true, new_predicted)
        FPR[i] = false_positive_rate(true, new_predicted)
    FPR[-1] = 1.
    TPR[-1] = 1.
    auc = auc_roc(true, predicted, TPR=TPR)
    label = label + " (auc={:.2f})".format(auc)
    ax.plot(FPR, TPR, label=label)
    ax.set_title("ROC curve")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.legend()
    #plt.show()
    return

"""
Returns the area under the ROC curve. True and predicted must be 1d arrays
This is calculated using the trapezoidal rule with the number of intervals equal to the precision parameter.
It can also be calculated from a true positive rate array already given.
"""
def auc_roc(true, predicted, TPR=None, precision=1000):
    if TPR is None:
        if true.shape[0]!=predicted.shape[0]:
            print(f"True and predicted must have same length but found {true.shape[0]} and {predicted.shape[0]}")
            return
        TPR = np.zeros(precision)
        thresholds = np.linspace(0, 1, precision)
        for i in range(-1, len(thresholds)-1):
            new_predicted = np.zeros(predicted.shape)
            new_predicted[np.argwhere(predicted>thresholds[i])] = 1
            TPR[i] = recall(true, new_predicted)
        TPR[-1] = 1.
    score = (1+2*(np.sum(TPR)-1))*(1/(2*TPR.shape[0]))
    return score

"""
Returns the log loss of the prediction. True and predicted must be 1d arrays
This is usually the loss function that the classifier tries to optimize
"""
def log_loss2(true, predicted):
    if true.shape[0]!=predicted.shape[0]:
        print(f"True and predicted must have same length but found {true.shape[0]} and {predicted.shape[0]}")
        return
    res = 0
    res -= np.sum(true*np.log(predicted))
    res -= np.sum((1-true)*np.log((1-predicted)))
    return res/true.shape[0]

"""
Returns the brier score. True and predicted must be 1d arrays
It is a measure of how far the predictions are from the truth, computed simply with the mean squared error divided by the number of observations.
"""
def brier_score(true, predicted):
    if true.shape[0]!=predicted.shape[0]:
        print(f"True and predicted must have same length but found {true.shape[0]} and {predicted.shape[0]}")
        return
    return np.sum((true-predicted)**2)/true.shape[0]







from sklearn.metrics import brier_score_loss
y_true = np.random.randint(2, size=1000)
y_pred = np.random.rand(1000)
print(brier_score_loss(y_true, y_pred))
print(brier_score(y_true, y_pred))
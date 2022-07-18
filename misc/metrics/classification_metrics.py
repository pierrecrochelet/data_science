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
def compute_basics(true, predicted, true_val = 1, false_val = 0):
    if true.shape[0]!=predicted.shape[0]:
        print(f"True and predicted must have same length but found {true.shape[0]} and {predicted.shape[0]}")
        return
    added = true+predicted
    subtracted = true-predicted
    Tp = np.argwhere(added==2*true_val).shape[0]
    Tn = np.argwhere(added==2*false_val).shape[0]
    Fp = np.argwhere(subtracted==false_val-true_val).shape[0]
    Fn = np.argwhere(subtracted==true_val-false_val).shape[0]
    return Tp, Tn, Fp, Fn

"""
Displays the confusion matrix. True and predicted must be 1d arrays
Gives to option to plot it in a given axis.
"""
def display_confusion_matrix(true, predicted, true_val = 1, false_val = 0, ax=None):
    Tp, Tn, Fp, Fn = compute_basics(true, predicted, true_val, false_val)
    
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
def compute_false_positive_rate(true, predicted, true_val = 1, false_val = 0):
    _, Tn, Fp, _ = compute_basics(true, predicted, true_val, false_val)
    return (Fp/(Fp+Tn))

"""
Returns the false negative rate (a.k.a. type 2 error). True and predicted must be 1d arrays
This is calculated as the number of false negatives (Fn) on the number of total positives (Tp+Fn)
In other words, it measures, out of all positives, how many the model has incorrectly identified as negatives.
"""
def compute_false_negative_rate(true, predicted, true_val = 1, false_val = 0):
    Tp, _, _, Fn = compute_basics(true, predicted, true_val, false_val)
    return (Fn/(Tp+Fn))

"""
Returns the true negative rate (a.k.a. specificity). True and predicted must be 1d arrays
This is calculated as the number of true negatives (Tn) on the number of total positives (Tp+Fn).
In other words, it measures, out of all negatives, how many the model has correctly identified as negatives.
"""
def compute_true_negative_rate(true, predicted, true_val = 1, false_val = 0):
    _, Tn, Fp, _ = compute_basics(true, predicted, true_val, false_val)
    return (Tn/(Fp+Tn))

"""
Returns the negative predicted value (a.k.a. precision for negative class). True and predicted must be 1d arrays
This is calculated as the number of true negatives (Tn) on the number of all predicted negatives (Tn+Fn).
In other words, it measures, out of all negative predictions, how many were actually negatives.
"""
def compute_negative_predicted_value(true, predicted, true_val = 1, false_val = 0):
    _, Tn, _, Fn = compute_basics(true, predicted, true_val, false_val)
    return (Tn/(Fn+Tn))

"""
Returns the false discovery rate. True and predicted must be 1d arrays
This is calculated as the number of false positives (Fp) on the number of all predicted positives (Fp+Tp).
In other words, it measures, out of all positive predictions, how many mistakes there are.
"""
def compute_false_discovery_rate(true, predicted, true_val = 1, false_val = 0):
    Tp, _, Fp, _ = compute_basics(true, predicted, true_val, false_val)
    return (Fp/(Tp+Fp))

"""
Returns the recall (a.k.a. true positive rate, a.k.a. sensitivity). True and predicted must be 1d arrays
This is calculated as the number of true positives (Tp) on the number of all positives (Tp+Fn).
In other words, it measures, out of all positives, how many were found by the model.
"""
def compute_recall(true, predicted, true_val = 1, false_val = 0):
    Tp, _, _, Fn = compute_basics(true, predicted, true_val, false_val)
    return (Tp/(Tp+Fn))

"""
Returns the precision (a.k.a. positive predicted value). True and predicted must be 1d arrays
This is calculated as the number of true positives (Tp) on the number of all predicted positives (Tp+Fp).
In other words, it measures, out of all predicted positives, how many actually positives.
"""
def compute_precision(true, predicted, true_val = 1, false_val = 0):
    Tp, _, Fp, _ = compute_basics(true, predicted, true_val, false_val)
    return (Tp/(Tp+Fp))

"""
Returns the accuracy. True and predicted must be 1d arrays
This is calculated as the number of true positives (Tp) and true negatives (Tn) on the number of all observations (Tp+Tn+Fn+Fp).
In other words, it measures, out of all samples, how many correctly classified.
"""
def compute_accuracy(true, predicted, true_val = 1, false_val = 0):
    Tp, Tn, Fp, Fn = compute_basics(true, predicted, true_val, false_val)
    return ((Tp+Tn)/(Tp+Tn+Fp+Fn))

"""
Returns the f1-score. True and predicted must be 1d arrays
This is calculated as precision times recall on precision added to recall.
In other words, it is a harmonic mean between precision and recall, giving both the same importance.
"""
def compute_f1_score(true, predicted, true_val = 1, false_val = 0):
    Tp, _, Fp, Fn = compute_basics(true, predicted, true_val, false_val)
    return ((2*Tp)/(2*Tp+Fp+Fn))

"""
Returns the f_beta score. True and predicted must be 1d arrays
This is a generalization of the f1 score. Here, the more you care about the recall over the precision, the higher beta should be.
"""
def compute_fBeta_score(true, predicted, beta, true_val = 1, false_val = 0):
    Tp, _, Fp, Fn = compute_basics(true, predicted, true_val, false_val)
    return ((Tp*(1+beta^2))/((Tp*(1+beta^2))+((beta^2)*Fn)+Fp))

"""
Returns the kappa statistic. True and predicted must be 1d arrays
This is calculated using observed_accuracy (the accuracy of the classifier) and expected accuracy (how well would a randoom classifier do looking at the confusion matrix). 
The latter is calculated looking at a percentage of time classifiers agree.
In other words, the kappa statistics measures how much better the classifier is than a random classifier. 
"""
def compute_kappa_statistics(true, predicted, true_val = 1, false_val = 0):
    Tp, Tn, Fp, Fn = compute_basics(true, predicted, true_val, false_val)
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
def compute_matthews_correlation_coefficient(true, predicted, true_val = 1, false_val = 0):
    Tp, Tn, Fp, Fn = compute_basics(true, predicted, true_val, false_val)
    numerator = (Tp*Tn)-Fp*Fn
    denominator = np.sqrt((Tp+Fp)*(Tp+Fn)*(Tn+Fp)*(Tn+Fn))
    return numerator/denominator

"""
Displays the receiver operating characteristic curve (a.k.a ROC curve). True and predicted must be 1d arrays
Roc is usually used to find the prediction boundary and therefore is better when used with continuous values, not with binary values as the other metrics.
Gives the option to plot it in a given axis with given label. Also, provides the degree of precision of the curve given as the number of points plotted
"""
def display_roc_curve(true, predicted, true_val = 1, false_val = 0, ax=None, label="classifier", precision=10000):
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
        TPR[i] = compute_recall(true, new_predicted, true_val, false_val)
        FPR[i] = compute_false_positive_rate(true, new_predicted, true_val, false_val)
    FPR[-1] = 1.
    TPR[-1] = 1.
    auc = compute_auc_roc(true, predicted, TPR=TPR)
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
def compute_auc_roc(true, predicted, true_val = 1, false_val = 0, TPR=None, precision=1000):
    if TPR is None:
        if true.shape[0]!=predicted.shape[0]:
            print(f"True and predicted must have same length but found {true.shape[0]} and {predicted.shape[0]}")
            return
        TPR = np.zeros(precision)
        thresholds = np.linspace(0, 1, precision)
        for i in range(-1, len(thresholds)-1):
            new_predicted = np.zeros(predicted.shape)
            new_predicted[np.argwhere(predicted>thresholds[i])] = 1
            TPR[i] = compute_recall(true, new_predicted, true_val, false_val)
        TPR[-1] = 1.
    score = (1+2*(np.sum(TPR)-1))*(1/(2*TPR.shape[0]))
    return score

"""
Returns the log loss of the prediction. True and predicted must be 1d arrays
This is usually the loss function that the classifier tries to optimize
"""
def compute_log_loss(true, predicted):
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
def compute_brier_score(true, predicted):
    if true.shape[0]!=predicted.shape[0]:
        print(f"True and predicted must have same length but found {true.shape[0]} and {predicted.shape[0]}")
        return
    return np.sum((true-predicted)**2)/true.shape[0]

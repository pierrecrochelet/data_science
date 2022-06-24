import numpy as np

"""
implementation of a scaler using normalization of features. 
The find_parameters(data) expects an array of (n_observations, n_features). 
It will iterate over all the features and compute the mean and variance of each then return them in array of (n_features, 2) where first element of each row is the mean and second is the std.
The scale_data(data, params) expects an array of (n_observations, n_features) as data and an array of (n_features, 2) as params.
It will transform the data array in-place so that each observation is normalized. Array should be declared of type float!!
I chose to make those in two seperate functions so that the first can be applied on training data and the second can be applied on training and test data with the parameters returned by the first.
"""
def find_parameters(data):
    params = np.empty((data.shape[1], 2))
    for i in range(0, data.shape[1]):
        params[i] = np.array([np.mean(data[:,i]), np.std(data[:, i])])
    return params

def scale_data(data, params):
    if params.shape[0]<data.shape[1]:
        print("not enough parameters compared to data features")
        return
    
    for i in range(0, data.shape[1]):
        mean = params[i, 0]
        std = params[i, 1]
        data[:,i] = (data[:,i]-mean)/std
if __name__=="__main__":
    data = np.array([[11, 12, 13, 14], [9, 10, 1, 2], [0, 1, 2, 3]], dtype=float)
    params = find_parameters(data)
    print(f"Data input was:\n{data}")
    print(f"Calculated parameters are:\n{params}")
    scale_data(data, params)
    print(f"Data after normalization is:\n{data}")
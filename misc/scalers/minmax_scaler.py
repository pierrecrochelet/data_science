import numpy as np
"""
implementation of a scaler using min and max to scale to specified range. 
The find_parameters(data) expects an array of (n_observations, n_features). 
It will iterate over all the features and find the min and max values of each then return them in array of (n_features, 2) where first element of each row is the min and second is the max.
The scale_data(data, params, new_data_range) expects an array of (n_observations, n_features) as data and an array of (n_features, 2) as params.
The new_data_range params can either be a 1D array of (n_features,) to apply same range to each features. Or it can be an array of (n_features, 2) to apply different ranges to each features.
It will transform the data array in-place so that each observation is scaled to the specified range. Array should be declared of type float!!
I chose to make those in two seperate functions so that the first can be applied on training data and the second can be applied on training and test data with the parameters returned by the first.
"""
def find_parameters(data):
    params = np.empty((data.shape[1], 2))
    for i in range(0, data.shape[1]):
        params[i] = np.array([np.min(data[:,i]), np.max(data[:, i])])
    return params

def scale_data(data, params, new_data_range):
    if params.shape[0]<data.shape[1]:
        print("not enough parameters compared to data features")
        return
    if len(new_data_range.shape)>1 and new_data_range.shape[0]<data.shape[1]:
        print("new_data_range should either be a 1D array to have all features in the same range or a 2D array of size (n_features, 2)")
        return
    for i in range(0, data.shape[1]):
        if len(new_data_range.shape)>1:
            this_min = new_data_range[i, 0]
            this_max = new_data_range[i, 1]
        else:
            this_min = new_data_range[0]
            this_max = new_data_range[1]
        data_min = params[i, 0]
        data_max = params[i, 1]
        data[:,i] = this_min + (this_max-this_min) * ((data[:,i]-data_min)/(data_max-data_min))

if __name__=="__main__":
    data = np.array([[11, 12, 13, 14], [9, 10, 1, 2], [0, 1, 2, 3]], dtype=float)
    params = find_parameters(data)
    print(f"Data input was:\n{data}")
    print(f"Calculated parameters are:\n{params}")
    scale_data(data, params, np.array([0, 1]))
    print(f"Data after normalization is:\n{data}")
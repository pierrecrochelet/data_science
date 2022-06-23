from copy import deepcopy
import numpy as np

my_array = np.random.rand(100)
"""
Implementation of merge sort. Takes advantage of the fact that it's easy to sort two sorted arrays. Therefore we'll break the array in two, until having arrays of size 1 and then merge.
This is not in-place as in-place version makes the time complexity worse. Time complexity of this is O(n log(n)) in worst-case.
"""

def mergesort(array):
    if len(array)<=1:
        return array
    res = np.array([])
    mid = len(array)//2
    left = mergesort(array[:mid])
    right = mergesort(array[mid:])

    i = 0
    j = 0
    while(i<len(left)):
        if j>=len(right):
            res = np.append(res, left[i])
            i+=1
        elif left[i]<=right[j]:
            res = np.append(res, left[i])
            i+=1
        else:
            res = np.append(res, right[j])
            j+=1
    while j<len(right):
        res = np.append(res, right[j])
        j+=1
    return res


print(my_array)
res = mergesort(my_array)
print(res)
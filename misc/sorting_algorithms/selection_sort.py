import numpy as np

my_array = np.random.rand(100)

"""
implementation of selective sort. At each iteration, goes through the whole array to find the lowest value then swap it in front
This has O(n^2) worst-case complexity.
"""

def selective_sort(array):
    for i in range(0, len(array)):
        min_index = i
        for j in range(i+1, len(array)):
            if array[j]<array[min_index]:
                min_index = j
        temp = array[i]
        array[i] = array[min_index]
        array[min_index] = temp

selective_sort(my_array)
print(my_array)

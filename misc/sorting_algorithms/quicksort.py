import numpy as np

counter = 0

my_array = np.random.rand(100)
"""

"""

def partition(array, low, high):
    global counter

    pivot = np.random.randint(low, high) # Choosing the pivot at random minimizes chances of worst-case scenario

    # Need to place pivot at the end or problems when iterating over elements
    temp = array[high]
    array[high] = array[pivot]
    array[pivot] = temp
    pivot = high

    i = low

    for j in range(low, high):
        if array[j]<array[pivot]:
            temp = array[i]
            array[i] = array[j]
            array[j] = temp
            i += 1
    if i<pivot:
        temp = array[i]
        array[i] = array[pivot]
        array[pivot] = temp
    return i

def quicksort(array, low, high):

    index = partition(array, low, high)

    if low<index-1:
        quicksort(array, low, index-1)
    if index+1<high:
        quicksort(array, index+1, high)

quicksort(my_array, 0, len(my_array)-1)
print(my_array)

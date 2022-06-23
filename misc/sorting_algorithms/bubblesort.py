import numpy as np

my_array = np.random.rand(100)
"""
implementation of bubble sort. The worst-case complexity of bubble sort is O(n^2) which happens if the smallest value is at the end of the array. 
The while loop will happen n times and the for loop always happens n-1 times, therefore O(n*(n-1))=O(n^2)
"""

def bubblesort(array):
    nbr_changes = -1
    while(nbr_changes!=0):
        nbr_changes = 0
        for i in range(1, len(array)):
            if array[i]<array[i-1]:
                temp = array[i]
                array[i] = array[i-1]
                array[i-1] = temp
                nbr_changes+=1

print(my_array)
bubblesort(my_array)
print(my_array)
"""
파일명: Ex21-01-BubbleSort.py

버블정렬(Bubble Sort)
    인접한 두 원소를 비교하여 정렬하는 알고리즘
    가장 간단한 정렬 알고리즘

    시간복잡도 O(n^2)
"""

def bubble_sort(arr):
    n = len(arr)

    '''
    arr = [1, 2, 3, 4, 5, 6]
    n = 6
    i: 0 ~ 5
    j: 0 ~ 4
    
    i = 0
        j = 0
        arr[0] > arr[1]
        j = 1
        arr[1] > arr[2]
        j = 2
        arr[2] > arr[3]
        j = 3
        arr[3] > arr[4] 
        j = 4
        arr[4] > arr[5] 
    i = 1
    i = 2
    
    '''

    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

    return arr

# 실행코드
arr = [6, 5, 3, 1, 2, 4]
print(bubble_sort(arr))









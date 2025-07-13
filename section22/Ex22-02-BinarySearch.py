"""
파일명: Ex22-02-BinarySearch.py

이진검색(Binary Search)
    데이터가 정렬되어 있는 상태에서 사용가능한 알고리즘
    중앙값과 비교하여 탐색 범위를 반으로 줄여가며 찾는 탐색 알고리즘
"""

def binary_search(arr, x):

    low = 0
    high = len(arr) - 1
    '''
    arr = [0, 4, 7, 10, 14, 23, 45, 47, 53]
    low = 7
    high = 8
    mid = 7
    x = 47
    '''
    while low <= high:
        mid = (low + high) // 2

        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1

# 실행코드
arr = [0, 4, 7, 10, 14, 23, 45, 47, 53]
print(binary_search(arr, 47))   # 7
"""
파일명: Ex20-02-O(logn).py

O(logN)
    로그 시간 복잡도, 이진 탐색처럼 절반으로 나누어 해결하는 알고리즘
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





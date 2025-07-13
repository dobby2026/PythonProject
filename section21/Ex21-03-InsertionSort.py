"""
파일명: Ex21-03-InsertionSort.py

삽입정렬(Insertion Sort)
    리스트의 모든 요소를 앞에서 부터 차례대로
    이미 정렬된 부분과 비교하여 자신의 위치를 찾아 삽입
"""

def insrtion_sort(arr):
    n = len(arr)

    """
    arr = [1, 2, 3, 5, 6, 4]
    n = 6 
    i: 1 ~ 5
    i = 2
    kye = 3
    j = -1
    arr[j] > key : 5 > 3
    arr[j + 1] = arr[j] :  arr[1] = arr[0]
    
    """

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

    return arr

# 실행코드
arr = [6, 5, 3, 1, 2, 4]
print(insrtion_sort(arr))




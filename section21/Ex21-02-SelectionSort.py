"""
파일명: Ex21-02-SelectionSort.py

선택정렬(Selection Sort)
    주어진 리스트에서 최소값을 찾아
    맨 앞에 잇는 값과 교체하는 알고리즘

"""

# 선택정렬 알고리즘
def selection_sort(arr):
    '''
    arr = [5, 4, 3, 1, 2]
    len(arr): 5
    i : 0 ~ 4
    '''

    for i in range(len(arr)):

        min_idx = i
        '''

        arr = [1, 2, 3, 4, 5]
        i = 1
        min_idx = 3
        range(i+1, len(arr) : 1 ~ 4
        j = 4
        '''

        for j in range(i + 1, len(arr)):

            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr


# 실행코드
arr = [5, 4, 3, 1, 2]
print(selection_sort(arr))
"""
파일명: Ex20-04-O(nlogn).py

O(NlogN)
    선형 로그 시간 복잡도, 병합 정렬 등의 알고리즘
"""

def merge_sort(arr):

    if len(arr) <= 1:
        return arr
    '''
    arr = [6, 5, 3, 1, 8, 7, 2, 4]
    mid = 4
    left = merge_sort(arr[:4])  -> [6, 5, 3, 1] -> return [1, 3, 5, 6]
        arr = [6, 5, 3, 1]
        mid = 2
        left = merge_sort(arr[:2])  -> [6, 5] -> return [5, 6]
            arr = [6, 5]
            mid = 1
            left = merge_sort(arr[:1])  -> [6] -> return [6]
            right = merge_sort(arr[1:]) -> [5] -> return [5]
            return [5, 6] 
        right = merge_sort(arr[2:]) -> [3, 1] -> return [1, 3]
            arr = [3, 1]
            mid = 1
            left = merge_sort(arr[:1])  -> [3] -> return [3]
            right = merge_sort(arr[1:]) -> [1] -> return [1]
            return [1, 3]
        return merge([5, 6], [1, 3]) => [1, 3, 5, 6]
        
    right = merge_sort(arr[4:]) ->  [8, 7, 2, 4] -> return [2, 4, 7, 8]
    
    return merge([1, 3, 5, 6], [2, 4, 7, 8]) -> [1, 2, 3, 4, 5, 6, 7, 8]
        
    '''

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):

    result = []
    i = j = 0

    '''
    merge([5, 6], [1, 3])
    left = [5, 6]
    right = [1, 3]
    result = [1, 3, 5, 6]
    i = 0
    j = 2
    
    '''
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result += left[i:]
    result += right[j:]
    return result

# 실행코드
arr = [6, 5, 3, 1, 8, 7, 2, 4]
sorted_arr = merge_sort(arr)
print(sorted_arr)


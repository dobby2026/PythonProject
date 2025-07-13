"""
파일명: Ex20-04-O(nlogn).py

O(NlogN)
    선형 로그 시간 복잡도, 병합 정렬 등의 알고리즘
"""

def merge_sort(arr):

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):

    result = []
    i = j = 0
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


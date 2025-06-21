"""
파일명: Ex09-01-built-in-function.py

내장함수
    파이썬에서 제공해주는 별도의 import 없이
    사용할 수 있는 함수
"""
# 리스트 관련 내장함수
numbers = [1, -5, 2, 3, -8, 3, 9, -3, 4, 7, -1]
print('1. 합계:', sum(numbers))
print('2. 최대값:', max(numbers))
print('3. 최소값:', min(numbers))
print('4. 정렬된 리스트:', sorted(numbers))
print('5. 역정렬 리스트:', sorted(numbers, reverse=True))
print('6. 리스트 길이:', len(numbers))
print('7. 절대값 맵핑:', list(map(abs, numbers))) # map(적용할함수, 반복가능한 객체)

# 수학 관련된 내장함수
print('1. 반올림:', round(3.7))
print('2. 절대값:', abs(-5))
print('3. 거듭제곱', pow(2, 3))

# 문자 관련 함수
print('1. ASCII 코드:', ord('A'))
print('2. ASCII to 문자:', chr(65))












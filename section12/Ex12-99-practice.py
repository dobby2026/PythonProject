"""
파일명: Ex12-99-practice.py

리스트 컴프리헨션(List Comprehension)
    기존 for 루프와 조건문을 한줄로 표현

    문법
        [표현식 for 항목 in 반복가능객체]
        [표현식 for 항목 in 반복가능객체 if 조건]
"""
# 일반 for 루프
numbers = []
for i in range(5):
    numbers.append(i * 2)
print(numbers)

# 리스트 컴프리헨션
numbers = [i * 2 for i in range(5)]
print(numbers)

# 리스트 컴프리헨션 (조건문)
numbers = [i for i in range(100) if i % 2 == 0]
print(numbers)


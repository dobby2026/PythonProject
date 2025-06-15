"""
파일명: Ex05-01-if.py

조건문
    특정 조건에 따라 다른 코드를 실행하도록 하는 제어문

    * 들여쓰기를 사용하여 코드의 범위 정의
"""
a = 100
b = 200
# if 문
if b > a:
    print('b는 a보다 크다.')

# if ~ else문
a = 7
b = 4
if b >= a:
    print('b는 a보다 크거나 같다.')
else:
    print('b는 a보다 작다.')

# if ~ elif ~ else
age = 15

if age >= 19:
    print('성인 입니다.')
elif age >= 13:
    print('청소년 입니다.')
elif age >= 8:
    print('어린이 입니다.')
else:
    print('영유아 입니다.')

print('프로그램 종료')












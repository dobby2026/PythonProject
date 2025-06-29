"""
파일명: Ex17-01-Exception.py
예외 (Exception)
    프로그램 실행중 발생할 수 있는 오류나 예기치 않은 상황
"""
a = int(input('제수를 입력하세요 >>> '))
b = int(input('피제수를 입력하세요 >>> '))

if b == 0:
    print('0으로 나누는 것은 불가능 합니다.')
else :
    print(f'{a} / {b} = {a / b}')



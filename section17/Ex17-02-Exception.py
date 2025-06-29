"""
파일명: Ex17-02-Exception.py

예외처리 방법
try:
    정상코드 영역
except:
    예외 발생시 처리 영역
"""

try:
    a = int(input('제수를 입력하세요 >>> '))
    b = int(input('피제수를 입력하세요 >>> '))
    print(f'{a} / {b} = {a / b}')
except:
    print('0으로 나눌 수 없습니다.')

print('프로그램 종료!')



"""
파일명: Ex13-03-appendFile.py

open 함수모드
    a(append mode): 추가 모드
"""
with open('hello.txt', 'at', encoding='UTF-8') as file:
    file.write('Hello\n')
    file.write('Nice to meet you\n')

print('hello.txt 파일에 새로운 내용이 추가 되었습니다.')



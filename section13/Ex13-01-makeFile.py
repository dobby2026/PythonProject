"""
파일명: Ex13-01-makeFile.py

I/O (Input/Output)
    외부와 데이터를 주고 받는 모든 작업
    I/O는 사용자 입력, 파일 처리, 네트워크 통신 등을 말한다

open() 함수
    파이썬에서 open()한수를 사용하여 파일을 열고 파일객체 생성,
    이를 통해 파일을 읽고 쓸 수 있다

"""

file = open('myFile.txt', 'wt')
print('myFile.txt 파일이 생성되었습니다.')
file.close()

# with문 - 자동으로 close()를 해준다
with open('myFile2.txt', 'wt') as file:
    print('myFile2.txt 파일이 생성되었습니다.')


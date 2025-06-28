"""
파일명: Ex13-04-readFile.py

open 함수 모드
    r(read mode): 읽기 전용 모드 / 파일 없으면 에러
"""
with open('hello.txt', 'rt', encoding='UTF-8') as file:
    '''
    f_str = file.read() # 전체 읽기
    print(f_str)
    '''

    while True:
        f_str = file.readline() # 한줄씩 읽기
        if not f_str:
            break
        print(f_str, end='')


print('파일읽기 종료')













"""
파일명: Ex14-01-copyFile.py

open 함수 모드 
    b(binary mode): 해당 파일의 데이터를 바이너리 파일로 인식 입출력
"""

buffer_size = 3
with open('../section13/hello.txt', 'rb') as org_file:
    with open('hello2.txt', 'wb') as copy_file:
        
        ''' 전체 읽기
        f_str = org_file.read() # 파일 전체를 메모리로
        copy_file.write(f_str) # 한 번에 전체 쓰기
        '''
        # 버퍼 방식
        while True:
            buffer = org_file.read(buffer_size)
            if not buffer:
                break
            print(buffer)
            copy_file.write(buffer)


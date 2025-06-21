"""
파일명: Ex08-02-nested-loop.py

중첩 반복문
    반복문 안에 반복문
"""
i = 0
while i < 7:
    '''
    i = 0, 1, 2, 3
    j = 0
    
    *
    **
    ***
    ****
    *****
    ******
    *******
    '''

    j = 0
    while j < i+1:
        print('*', end='')
        j += 1

    print()
    i += 1


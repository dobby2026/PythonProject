"""
파일명: Ex08-01-break.py

break 문
    while 문이나 for 문과 같은 반복문을
    강제로 종료하는 제어문

Ctrl + Shift + F10
"""

n = 1
while True:
    print(n)
    if n == 100:
        break

    n += 1

print('main 종료')





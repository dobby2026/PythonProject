"""
파일명: Ex08-04-continue.py

continue
    while문이나 for문과 같은 반복문을 강제로 건너뛰게 한다
"""

total = 0

for n in range(1, 101):
    if n % 3 == 0:
        continue
    total += n
    print(f'n: {n}, total: {total}')



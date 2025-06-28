"""
파일명: Ex12-88-practice.py
"""
import random
import time

pot = [n for n in range(1, 46)]

jackpot = []

for n in range(1, 7):
    random.shuffle(pot)

    pick = pot.pop()
    print(f'{n}번째 번호는 {pick} 입니다.')
    jackpot.append(pick)
    time.sleep(2)
# [2, 10, 17, 23, 27, 31]
# [8, 11, 13, 32, 36, 40]
# [3, 19, 22, 28, 37, 40]
# [9, 17, 18, 20, 41, 45]
# [24, 26, 33, 36, 38, 41]
jackpot.sort()
print(jackpot)
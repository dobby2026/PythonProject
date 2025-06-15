"""
파일명: Ex05-02-if.py
"""

import random

choices = ['가위', '바위', '보']

computer = random.choice(choices)

# 사용자 입력받기
print('가위, 바위, 보 중 하나를 선택하세요!')

player = input('당신의 선택은? ')
print(f'\n플레이어: {player}')
print(f'컴퓨터: {computer}')

# 승부 판정
if player == computer:
    print('비겼습니다!')
elif player == '가위':
    if computer == '보':
        print('이겼습니다!')
    else:
        print('졌습니다ㅠ')
elif player == '바위':
    if computer == '가위':
        print('이겼습니다!')
    else:
        print('졌습니다ㅠ')
elif player == '보':
    if computer == '바위':
        print('이겼습니다!')
    else:
        print('졌습니다ㅠ')
else:
    print('잘못된 입력입니다.')

    
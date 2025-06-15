"""
파일명: Ex04-01-arithmetic.py

연산자
    변수나 값에 대해 특정한 연산을 수행하는 기호나 키워드

1. 산술 연산자
    기본적인 수학 연산수행
    +, -, *(곱하기), /(나누기), //(몫), %(나머지), **(거듭제곱)
"""

# 1. 기본 연산
level = 15
exp = 220

print(f'레벨 업: {level + 1}')    # 덧셈
print(f'경험치 감소: {exp - 50}')  # 뺄셈
print(f'2배 경험치: {exp * 2}')    # 곱셈
print(f'레벨 제곱: {level **2}')   # 거듭제곱

# 2. 뺄셈 - 데미지 계산
damage = 75
defense = 30
actual_damage = damage - defense
print(f'실제 데미지: {actual_damage}')

# 3. 몫, 나머지 - 아이템 분배
potions = 15
team_size = 4

per_member = potions // team_size   # 몫: 팀원당 개수
remainder = potions % team_size     # 나머지: 남는 개수

print(f'팀원당 포션: {per_member}')
print(f'남는 포션: {remainder}')

# 4. 비율 계산
max_hp = 100
current_hp = 37
hp_ratio = current_hp / max_hp * 100
print(f'현재 체력: {hp_ratio:.1f}%')
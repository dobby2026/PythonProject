"""
파일명: Ex04-03-comprison.py

관계 연산자 (비교 연산자)
    두 값을 비교하여 bool 값 반환
    >, >=, <, <=, ==, !=

    is 연산자
        두 객체가 동일한 메모리 주소를 가리키는지 비교
    is not 연산자
        두 객체 메모리 주소가 같지 않을 경우 True
        
"""
# 레벨 비교
pikachu_lv = 25
charmander_lv = 20

print(f'피카츄 레벨 > 파이리 레벨: {pikachu_lv > charmander_lv}')

# 2. 타입 비교
type1 = "불꽃"
type2 = "물"
print(f'같은 타입? {type1 == type2}')

# 3.is 연산자
x = [1, 2, 3]
y = [1, 2, 3]
z = x
print(f'x == y: {x == y}')
print(f'x != y: {x != y}')
print(f'x is y: {x is y}')
print(f'x is z: {x is z}')
print(f'x is z: {x is not z}')









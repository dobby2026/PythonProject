"""
파일명: Ex04-06-conditions.py

조건 연산자(삼항 연산자)
    조건식 결과에 따라 참 또는 거짓의 결과를 반환한다
    참 if 조건식 else 거짓
"""
a = 20
b = 100
result = (a - b) if (a >= b) else (b - a)
print(f'a와 b의 차이는 {result}입니다.')


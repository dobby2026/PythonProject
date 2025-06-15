"""
파일명: Ex04-05-bitwise.py

비트 연산자
    이진수의 비트 단위 연산자

    & (AND): 두 비트 모두 1일 때 1
    | (OR) : 두 비트 중 하나라도 1이면 1
    ^ (XOR): 두 비트가 다르면 1
    ~ (NOT): 비트 반전

    << (LEFT SHIFT) : N칸 왼쪽 비트 이동
    >> (RIGHT SHIFT) : N칸 오른쪽 비트 이동

"""
a = 6   # 0 0110 -(not)-> 1 1001
b = 5   # 0 0101

print(f'a & b: {a & b}')
print(f'a | b: {a | b}')
print(f'a ^ b: {a ^ b}')
print(f'~a: {~a}')

print(f'a << 1: {a << 1}')  # 0 1100
print(f'a >> 1: {a >> 1}')  # 0 0011








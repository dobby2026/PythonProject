"""
파일명: Ex10-01-method-string.py

메서드(method)
    특정 객체가 가지고 있는 함수를 의미
    객체.메서드()

객체란
    프로그래밍에서 데이터(속성)와 기능을 하나로 묶은 단위
    ex) 물리적 - 컴퓨터, 자동차, 휴대폰
        논리적 - 주문정보, 영수증, 포켓몬
"""
# String 객체 format 메서드
'''
콜론(:) 포맷 지정자
{ : < 10 d }
    {}: 변수 위치
    : : 포맷 지정자 시작 구분자
    < : 왼쪽 정렬
    10: 총 자릿수(폭)
    d : decimal (10진 정수) 
'''
print('10자리 폭 왼 쪽 정렬 "{:<10d}"'.format(123))
print('10자리 폭 오른쪽 정렬 "{:>10d}"'.format(123))
print('10자리 폭 가운데 정렬 "{:^10d}"'.format(123))

print('10자리 폭 왼 쪽 정렬 채움문자 "{:*<10d}"'.format(123))
print('10자리 폭 오른쪽 정렬 채움문자 "{:*>10d}"'.format(123))
print('10자리 폭 가운데 정렬 채움문자 "{:*^10d}"'.format(123))

# join 메서드
s = '-'.join('python') # p-y-t-h-o-n
print(s)
s = '+'.join(['a', 'b', 'c', 'd', 'e'])
print(s)
s = ''.join(['a', 'b', 'c', 'd', 'e'])
print(s)

# split() 메서드
phone = '010-1234-5678'
result = phone.split('-')
print(result)    # ['010', '1234', '5678']
print(f'010-****-{result[2]}')

# strip(), lstrip(), rstrip() 공백제거 메서드
s = '     apple     '
result = s.strip()
print(result)

s = '     apple     '
result = s.lstrip()
print(result)

s = '     apple     '
result = s.rstrip()
print(result)

s = 'Life is to short'
result = s.replace('short', 'long')
print(result)













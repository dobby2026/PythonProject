"""
Ex17-04-Exception.py


"""

try:
    print('서버 연결 성공!')
    a = int(input('제수를 입력하세요 >>> '))
    b = int(input('피제수를 입력하세요 >>> '))
    result = a / b
except ZeroDivisionError as zde:
    print('0으로 나눌 수 없습니다.')
    print(zde)
except ValueError as ve:
    print('정수만 입력할 수 있습니다')
    print(ve)
except:
    print('예외가 발생했습니다.')
else:   # 예외가 발생하지 않으면 실행
    print(f'{a} / {b} = {result}')
finally:    # 항상 실행되는 영역
    print('서버 Close 성공!')
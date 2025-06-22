"""
파일명: Ex11-03-function.py

return
    함수는 작업을 수행한 결과를 반환(return)할 수 있다
    반환된 값은 함수 호출한 위치에서 사용할 수 있다

"""
# 매개변수 없음, 리턴 값 있음
def address():
    addr = '우편번호 12345\n'
    addr += '서울시 영등포구 여의도동'
    return addr

result = address() # result = '우편번호 12345\n서울시 영등포구 여의도동'
print(result)
# print(address())

# 매개변수 있음, 리턴 값 있음
'''
디폴트 매개변수(Default Parameter)
    함수 정의시 매개변수에 미리 값을 할당해 놓는것으로,
    함수 호출 시 해당 인수를 생략하면 기본값이 사용된다

기본값이 없는 매개변수가 기본값이 있는 
매개변수보다 앞에 와야 한다
'''
def plus(num1 = 10, num2 = 0):
    return num1 + num2

result = plus(20, 30)
print(result)


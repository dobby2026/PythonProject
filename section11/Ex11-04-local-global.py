"""
파일명: Ex11-04-local-global.py

지역변수(Local Variable)
    함수 내부에서 선언된 변수로, 해당 함수 안에서만 사용 가능
    함수가 종료되면 변수는 소멸된다

전역변수(Global Variable)
    함수 외부에서 선언된 변수로, 프로그램 전체에서 사용 가능
    함수 내부에서도 사용할 수 있지만, 함수 내부에서 변경하려면
    'global' 키워드를 사용해야한다
"""

# 전역변수 선언
gvar = '전역'

def globalAndLocal():
    # 지역변수 선언
    lvar = '지역'

    global gvar
    gvar = '변경된 전역'

    print(f'{gvar} 변수 입니다.')
    print(f'{lvar} 변수 입니다.')

globalAndLocal()
print(gvar)






















"""
파일명: Ex07-01-for.py

for 문
    반복 가능한 객체의 요소들을 하나씩 꺼내서 반복실행하는 반복문

    ex)
        for 변수 in 반복가능한 객체
            반복 수행할 코드

in 연산자
    특정 값이 컨테이너(리스트, 문자열, 튜플 등) 안에 포함 여부 확인
    True/False 반환

    ex) 값 in 컨테이너   # True 또는 False 반환

반복문에서 in 연산자
    반복할 요소들을 하나씩 꺼내오는 역할


"""
# 리스트를 사용한 반복
fruits = ['사과', '바나나', '딸기', '오렌지']
for fruit in fruits:
    '''
    1번째 반복
    fruit = fruits[0]
    2번째 반복
    fruit = fruits[1]
    3번째 반복
    fruit = fruits[2]
    4번째 반복
    fruit = fruits[3]
    '''
    
    print(fruit, end=' ')







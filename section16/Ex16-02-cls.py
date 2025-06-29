"""
파일명: Ex16-02-cls.py

클래스 변수
    클래스를 기반으로 만든 모든 인스턴스가 공유할 수 있는 변수

인스턴스(멤버) 변수
    해당 객체(인스턴스)만 사용하는 변수

클래스 메서드
    객체(인스턴스)가 없어도 클래스를 이용해 호출할 수 있다
    cls 키워드를 이용해 클래스를 메서드 안에서 클래스 변수 접근가능

"""

class Bag:

    count = 0   # 클래스 변수

    def __init__(self, no):
        Bag.count += 1
        self.no = no

    @classmethod    # @ 표시 데코레이터
    def sell(cls):
        cls.count -= 1

    @classmethod
    def remain_bag(cls):
        return cls.count

    @staticmethod
    def slogan():
        print('명품 주인을 찾습니다.')


# 실행코드
Bag.slogan()

print(f'Bag.count: {Bag.count}')
bag1 = Bag(1)
print(f'Bag.count: {Bag.count}')
bag2 = Bag(2)
print(f'Bag.count: {Bag.count}')
bag3 = Bag(3)
print(f'Bag.count: {Bag.count}')
print(f'bag1.no: {bag1.no}')
print(f'bag2.no: {bag2.no}')
print(f'bag3.no: {bag3.no}')

Bag.sell()
print(f'Bag.count: {Bag.remain_bag()}')













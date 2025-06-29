"""
파일명: Ex16-03-inheritance.py

상속 (Inheritance)
    상위클래스(슈퍼, 부모)가 가지고 있는 기능을
    그대로 물려받아 하위클래스(서브, 자식)에서
    사용할 수 있다

super()
    부모 클래스의 메서드나 속성을 호출할 때 사용하는 내장 클래스
"""
# 슈퍼클래스, 부모클래스
class Coffee:

    def __init__(self, bean):
        self.bean = bean

    def coffee_info(self):
        print(f'원두: {self.bean}')

# 서브클래스, 자식클래스
class Espresso(Coffee):

    def __init__(self, bean, water):
        super().__init__(bean)
        self.water = water

    def espress_info(self):
        super().coffee_info()
        print(f'물: {self.water}ml')


# 실행코드
coffee = Espresso('콜롬비아', 30)
coffee.espress_info()

print(f'원두: {coffee.bean}')
print(f'물: {coffee.water}')

coffee.coffee_info()












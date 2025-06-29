"""
파일명: Ex16-01-constructor-destructor.py

생성자 (Constructor)
    객체가 생성할 때 생성자가 자동으로 호출된다
    주로 객체 초기화 목적으로 사용

    생성자 선언 방법
        def __init__(self)

소멸자 (Destructor)
    객체가 소멸될 때 자동으로 호출된다

    소멸자 선언 방법
        def __del__(self)

"""
class USB:

    def __init__(self, capacity = '128G'):
        self.capacity = capacity
        print('USB 생성자 입니다.')

    def __del__(self):
        print(f'{self.capacity} USB를 파기합니다.')


# 실행코드
usb1 = USB()
print(f'usb1 : {usb1.capacity} USB 입니다.')

usb2 = USB('256G')
print(f'usb2 : {usb2.capacity} USB 입니다.')







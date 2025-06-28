"""
파일명: Ex15-01-object.py

클래스 (Class)
    클래스는 객체를 생성하기 위한 설계도 또는 틀 템플릿

    붕어빵 틀, 와플 기계

객체란
    프로그래밍에서 데이터(속성)와 기능을 하나로 묶은 단위
    ex) 물리적 - 컴퓨터, 자동차, 휴대폰
        논리적 - 주문정보, 영수증, 포켓몬
"""
class Computer:

    def set_spec(self, cpu, ram, vga, ssd):
        self.cpu = cpu
        self.ram = ram
        self.vga = vga
        self.ssd = ssd

    def hardware_info(self):
        print(f'CPU = {self.cpu}')
        print(f'RAM = {self.ram}')
        print(f'VGA = {self.vga}')
        print(f'SSD = {self.ssd}')

desktop = Computer()    # Computer 객체 생성
desktop.set_spec('i7', '32G', 'RTX 4060', '1T')
desktop.hardware_info()





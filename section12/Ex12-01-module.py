"""
파일명: Ex12-01-module.py

모듈(module)
    변수나 함수 또는 클래스를 모아 놓은 파일을 모듈이라고 한다

모듈 사용법
import 모듈명

패키지(Package)
    여러 모듈을 하나의 폴더에 담는 것을 패키지라고 한다

라이브러리(Library)
    특정 목적을 위한 패키지들의 집합
    보통 외부에서 설치해서 사용한다

"""
import converter

miles = converter.kilometer_to_miles(150)
print(f'150km = {miles}miles')

pound = converter.gram_to_pound(1000)
print(f'1000g = {pound}pounds')









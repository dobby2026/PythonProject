"""
파일명: Ex12-03-module.py

as(alias) 키워드 별명 사용하기
"""

import converter as cvt
from converter import kilometer_to_miles as k_to_m

miles = cvt.kilometer_to_miles(150)
print(f'150km = {miles}miles')

miles2 = k_to_m(150)
print(f'150km = {miles2}miles')


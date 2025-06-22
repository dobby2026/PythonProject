"""
파일명: Ex12-7-external.py

pip - 패키지 관리 도구
    PyPI(Python Package Index)에서 패키지를 다운로드 한다
    수많은 오픈소스가 저장되어 있는 중앙 저장소

패키지 설치 명령어
    pip install 패키지명

패키지 삭제 명령어
    pip uninstall 패키지명
"""
# 행렬 연산 관련 package
import numpy as np  # pip install numpy

print(np.sum([1, 2, 3, 4, 5]))

# 1차원 배열 두개 생성
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

c = a + b
print(c)

c = a - b
print(c)






"""
파일명: Ex23-01-matplotlib.py

데이터 시각화
    데이터를 분석한 결과를 사용자가 쉽게 이해할 수 있도록
    표현하여 전달하는것을 의미한다

모듈설치
pip install matplotlib

"""

import matplotlib.pyplot as plt


# Figure(도화지) 객체 생성 - 그래프를 그릴 전체 캔버스 생성
figure = plt.figure()

# subplot 생성(1행 1열 1번째 위치에 axes 생성)
axes = figure.add_subplot(111)

x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun' ]
y = [1200, 800, 500, 400, 700, 800]

axes.plot(x, y, linestyle='--', marker='^', color='red')

plt.show()








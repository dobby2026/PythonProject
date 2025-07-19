"""
파일명: Ex23-04-matplotlib.py
"""

import random
import matplotlib.pyplot as plt

figure = plt.figure()

axes = figure.add_subplot(1,2,1)

axes2 = figure.add_subplot(1,2,2)

x = [n for n in range(101)]

y1 = []
y2 = []

for i in range(101):
    #  0 ~ 100 사이의 난수 추가
    y1.append(random.randint(0,100))
    y2.append(random.randint(0,100))

# 선그래프
axes.plot(x, y1, color='r', marker='.')

# 막대그래프
axes2.bar(x, y2, color='g')

# 그래프 이미지 저장
plt.savefig('graph.png')

plt.show()









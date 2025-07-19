"""
파일명: Ex23-02-matplotlib.py
"""
import matplotlib.pyplot as plt

# Figure와 Axes 객체 동시생성
fig, ax = plt.subplots()

# 데이터 설정
fruits = ["apple", "blueberry", "cherry", 'orange']
count = [40, 100, 30, 55]
# 각 막대의 레이블(범례 표시될 레이블 - _red 범례 제외)
bar_labels = ["red", "blue", "_red", "orange"] 
# 각 막대의 색상
bar_colors = ["tab:red", "tab:blue", "tab:red", "tab:orange"]

ax.bar(fruits, count, color=bar_colors, label=bar_labels)

ax.set_ylabel("fruit supply")
ax.set_title("Fruit supply by kind and color")

ax.legend(title="fruit color")

plt.show()


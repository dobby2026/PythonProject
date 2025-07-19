import tkinter as tk
import random

def generate_lotto_numbers():
    numbers = random.sample(range(1, 46), 6)  # 1~45 중 중복 없이 6개 선택
    numbers.sort()
    result_label.config(text="로또 번호: " + ", ".join(map(str, numbers)))

# 메인 윈도우 생성
root = tk.Tk()
root.title("로또 번호 생성기")
root.geometry("300x200")
root.resizable(False, False)

# 라벨
title_label = tk.Label(root, text="🎉 로또 번호 생성기 🎉", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# 결과 표시 라벨
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

# 버튼
generate_button = tk.Button(root, text="번호 생성", command=generate_lotto_numbers, font=("Arial", 12), bg="#4CAF50", fg="white")
generate_button.pack(pady=10)

# GUI 루프 시작
root.mainloop()

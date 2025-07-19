'''
파일명: Ex24-07-Tkinter-TAB.py

Tkinter 간단한 TAB 예제

모듈 설치
pip install sv_ttk
'''
import tkinter as tk
from tkinter import ttk
import sv_ttk


class SimpleNotebookApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("간단한 노트북 예제")
        self.root.geometry("400x300")

        sv_ttk.set_theme("light")  # 다크 테마 적용

        self.setup_ui()

    def setup_ui(self):
        # 메인 프레임 생성
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill='both', expand=True)

        # 노트북(탭) 생성
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)

        # 첫 번째 탭
        tab1 = ttk.Frame(notebook)
        label1 = ttk.Label(tab1, text="첫 번째 탭의 내용입니다.")
        label1.pack(padx=20, pady=20)
        notebook.add(tab1, text="탭 1")

        # 두 번째 탭
        tab2 = ttk.Frame(notebook)
        label2 = ttk.Label(tab2, text="두 번째 탭의 내용입니다.")
        label2.pack(padx=20, pady=20)
        notebook.add(tab2, text="탭 2")

        # 세 번째 탭
        tab3 = ttk.Frame(notebook)
        label3 = ttk.Label(tab3, text="세 번째 탭의 내용입니다.")
        label3.pack(padx=20, pady=20)
        notebook.add(tab3, text="탭 3")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SimpleNotebookApp()
    app.run()
'''
파일명: Ex24-06-Tkinter-FileDialog.py
'''

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title('파일 다이아로그 예제')

# 버튼 프레임
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

def open_file():
    file_path = filedialog.askopenfilename(
        title='파일열기',
        filetypes=(('텍스트 파일', '*.txt'),
                   ('모든 파일', '*.*'))
    )

    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(
        title='파일 저장',
        defaultextension='.txt',
        filetypes=(('텍스트 파일', '*.txt'),
                   ('모든 파일', '*.*'))
    )

    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_area.get(1.0, tk.END))


tk.Button(button_frame, text='파일 열기', command=open_file).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text='파일 저장', command=save_file).pack(side=tk.LEFT, padx=5)

# 텍스트 영역
text_area = tk.Text(root, width=40, height=10)
text_area.pack(padx=10, pady=5)

root.mainloop()








"""
파일명: Ex24-01-Tkinter.py

tkinter
    python에서 기본적으로 제공하는 GUI 프로그램 모듈
"""
import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()

# 레이블 위젯 생성
label = tk.Label(root, text='Hello, Tkinter!')
label.pack()    # 위젯을 윈도우에 배치

# 한줄 입력 위젯 생성(단일 라인 텍스트 입력)
entry = tk.Entry(root)
entry.pack()

# 여러 줄 텍스트 입력 위젯 생성(멀티 라인 텍스트 입력)
text = tk.Text(root)
text.pack()

# 체크박스 위젯 생성
check_var = tk.IntVar() # 체크박스 상태를 저장할 변수(0: 체크 안됨, 1: 체크됨)
check_button = tk.Checkbutton(root, text='Check me!', variable=check_var)
check_button.pack()

# 라디오버튼 위젯 생성
radio_var = tk.StringVar()
radio_var.set('option1')
radio_button1 = tk.Radiobutton(root, text='Option 1', variable=radio_var,
                              value='option1')
radio_button2 = tk.Radiobutton(root, text='Option 2', variable=radio_var,
                              value='option2')
radio_button1.pack()
radio_button2.pack()

# 수평 슬라이더 위젯
scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
scale.pack()

# 스핀박스 위젯 생성
spinbox = tk.Spinbox(root, from_=0, to=100)
spinbox.pack()

# 콤보박스
combo = ttk.Combobox(root, values=['Option 1', 'Option 2', 'Option 3'])
combo.set('Option 1')
combo.pack()

def onClick():
    print('Button Click!')

    # 각 위젯의 현재 값을 가져오기
    s_entry = entry.get()

    # Text 위젯 모든 텍스트(1행 0열부터 끝까지)
    s_text = text.get('1.0', tk.END)

    i_check = check_var.get()
    s_radio = radio_var.get()
    i_scale = scale.get()
    i_spinbox = spinbox.get()
    s_combo = combo.get()

    # 가져온 값들 출력
    print(f's_entry: {s_entry}')
    print(f's_text: {s_text}')
    print(f'i_check: {i_check}')
    print(f's_radio: {s_radio}')
    print(f'i_scale: {i_scale}')
    print(f'i_spinbox: {i_spinbox}')
    print(f's_combo: {s_combo}')


button = tk.Button(root, text='Click!', command=onClick)
button.pack()


# 실행코드
if __name__ == '__main__':  # main 코드
    root.mainloop()


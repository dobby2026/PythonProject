import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ----------------- DB 초기화 -----------------
def init_db():
    conn = sqlite3.connect("board.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            writer TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ----------------- 글 목록 불러오기 -----------------
def load_posts(search_keyword=""):
    conn = sqlite3.connect("board.db")
    c = conn.cursor()
    if search_keyword:
        c.execute("SELECT id, title, writer, created_at FROM posts WHERE title LIKE ? ORDER BY id DESC",
                  (f'%{search_keyword}%',))
    else:
        c.execute("SELECT id, title, writer, created_at FROM posts ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

# ----------------- 글 작성 -----------------
def insert_post(title, content, writer):
    conn = sqlite3.connect("board.db")
    c = conn.cursor()
    c.execute("INSERT INTO posts (title, content, writer, created_at) VALUES (?, ?, ?, ?)",
              (title, content, writer, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

# ----------------- 글 상세 보기 -----------------
def get_post(post_id):
    conn = sqlite3.connect("board.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    post = c.fetchone()
    conn.close()
    return post

# ----------------- 글 수정 -----------------
def update_post(post_id, title, content, writer):
    conn = sqlite3.connect("board.db")
    c = conn.cursor()
    c.execute("UPDATE posts SET title=?, content=?, writer=? WHERE id=?", (title, content, writer, post_id))
    conn.commit()
    conn.close()

# ----------------- 글 삭제 -----------------
def delete_post(post_id):
    conn = sqlite3.connect("board.db")
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()
    conn.close()

# ----------------- GUI -----------------
class BoardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 블랙 게시판 (Tkinter + SQLite)")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#23272e")

        # 상단 Frame: 검색 & 새글 버튼
        top_frame = tk.Frame(self.root, bg="#23272e")
        top_frame.pack(fill=tk.X, pady=(20, 0))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            top_frame, textvariable=self.search_var, width=35, font=("맑은 고딕", 18),
            bg="#1a1c20", fg="#f8f9fa", insertbackground="#f8f9fa", relief=tk.FLAT
        )
        search_entry.pack(side=tk.LEFT, padx=(30, 15), ipady=8)

        tk.Button(
            top_frame, text="🔍 검색", command=self.search_posts, font=("맑은 고딕", 16, "bold"),
            bg="#353b48", fg="#00a8ff", relief=tk.FLAT,
            activebackground="#2f3640", activeforeground="#00a8ff",
            width=10, height=2
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            top_frame, text="새 글쓰기", command=self.show_write_popup, font=("맑은 고딕", 16, "bold"),
            bg="#192a56", fg="#fbc531", relief=tk.FLAT,
            activebackground="#273c75", activeforeground="#fbc531",
            width=12, height=2
        ).pack(side=tk.RIGHT, padx=30)

        # 글 목록 Treeview 스타일
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Treeview.Heading",
            font=("맑은 고딕", 16, "bold"),
            background="#353b48", foreground="#fbc531"
        )
        style.configure(
            "Treeview",
            rowheight=44, font=("맑은 고딕", 16),
            background="#23272e", fieldbackground="#23272e", foreground="#f8f9fa",
            borderwidth=0
        )
        style.map("Treeview", background=[('selected', '#273c75')])

        columns = ("id", "title", "writer", "created_at")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", style="Treeview")
        self.tree.heading("id", text="No")
        self.tree.heading("title", text="제목")
        self.tree.heading("writer", text="작성자")
        self.tree.heading("created_at", text="작성일")
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("title", width=540)
        self.tree.column("writer", width=130, anchor="center")
        self.tree.column("created_at", width=180, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=24, padx=30)

        self.tree.bind("<Double-1>", self.show_detail_popup)

        # 하단 버튼
        bottom_frame = tk.Frame(self.root, bg="#23272e")
        bottom_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Button(
            bottom_frame, text="🔄 새로고침", command=self.refresh_posts, font=("맑은 고딕", 16, "bold"),
            bg="#353b48", fg="#00a8ff", relief=tk.FLAT,
            activebackground="#2f3640", activeforeground="#00a8ff",
            width=12, height=2
        ).pack(side=tk.LEFT, padx=30)

        self.refresh_posts()

    # 글 목록 새로고침
    def refresh_posts(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in load_posts():
            self.tree.insert('', tk.END, values=row)

    # 글 검색
    def search_posts(self):
        keyword = self.search_var.get()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in load_posts(keyword):
            self.tree.insert('', tk.END, values=row)

    # 글쓰기 팝업
    def show_write_popup(self):
        self.popup_window("새 글쓰기", save_callback=self.write_post)

    def write_post(self, title, content, writer, window):
        if not (title and content and writer):
            messagebox.showwarning("입력 오류", "모든 항목을 입력해주세요.")
            return
        insert_post(title, content, writer)
        window.destroy()
        self.refresh_posts()

    # 상세/수정/삭제 팝업
    def show_detail_popup(self, event):
        item = self.tree.focus()
        if not item:
            return
        post_id = self.tree.item(item)["values"][0]
        post = get_post(post_id)
        if not post:
            return

        def save_update(title, content, writer, window):
            if not (title and content and writer):
                messagebox.showwarning("입력 오류", "모든 항목을 입력해주세요.")
                return
            update_post(post_id, title, content, writer)
            window.destroy()
            self.refresh_posts()

        def delete_and_close(window):
            if messagebox.askyesno("삭제 확인", "정말 삭제하시겠습니까?"):
                delete_post(post_id)
                window.destroy()
                self.refresh_posts()

        self.popup_window("글 상세/수정", post, save_update, delete_and_close)

    # 팝업 윈도우 (행 분리, scroll, 단축키, 중앙배치)
    def popup_window(self, title, post=None, save_callback=None, delete_callback=None):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("780x720")
        win.minsize(640, 600)
        win.configure(bg="#23272e")

        # 행 가중치: Text가 있는 행(3)만 확장
        # 0: 제목라벨 / 1: 제목엔트리 / 2: 내용라벨 / 3: 내용텍스트 / 4: 작성자라벨 / 5: 작성자엔트리 / 6: 버튼프레임
        win.grid_rowconfigure(3, weight=1)
        win.grid_columnconfigure(0, weight=1)

        label_fg = "#f8f9fa"
        entry_bg = "#1a1c20"
        entry_fg = "#fbc531"

        # 0행: 제목 라벨
        tk.Label(win, text="제목", font=("맑은 고딕", 18, "bold"),
                 bg="#23272e", fg=label_fg).grid(row=0, column=0, sticky="w",
                                               padx=32, pady=(30, 4))

        # 1행: 제목 Entry
        title_var = tk.StringVar(value=post[1] if post else "")
        title_entry = tk.Entry(win, textvariable=title_var, font=("맑은 고딕", 17, "bold"),
                               bg=entry_bg, fg=entry_fg, insertbackground=entry_fg,
                               relief=tk.FLAT)
        title_entry.grid(row=1, column=0, sticky="ew", padx=32, pady=(0, 16), ipady=10)

        # 2행: 내용 라벨
        tk.Label(win, text="내용", font=("맑은 고딕", 18, "bold"),
                 bg="#23272e", fg=label_fg).grid(row=2, column=0, sticky="w",
                                               padx=32, pady=(0, 4))

        # 3행: Text + Scrollbar
        text_frame = tk.Frame(win, bg="#23272e")
        text_frame.grid(row=3, column=0, sticky="nsew", padx=32, pady=(0, 16))
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        content_text = tk.Text(text_frame, font=("맑은 고딕", 16),
                               bg=entry_bg, fg=label_fg,
                               insertbackground=entry_fg, relief=tk.FLAT,
                               wrap="word")
        content_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(text_frame, orient="vertical",
                                 command=content_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        content_text.configure(yscrollcommand=scrollbar.set)

        if post:
            content_text.insert(tk.END, post[2])

        # 4행: 작성자 라벨
        tk.Label(win, text="작성자", font=("맑은 고딕", 18, "bold"),
                 bg="#23272e", fg=label_fg).grid(row=4, column=0, sticky="w",
                                               padx=32, pady=(0, 4))

        # 5행: 작성자 Entry
        writer_var = tk.StringVar(value=post[3] if post else "")
        writer_entry = tk.Entry(win, textvariable=writer_var, font=("맑은 고딕", 17, "bold"),
                                bg=entry_bg, fg=entry_fg, insertbackground=entry_fg,
                                relief=tk.FLAT)
        writer_entry.grid(row=5, column=0, sticky="ew", padx=32, pady=(0, 20), ipady=10)

        # 6행: 버튼 프레임
        btn_frame = tk.Frame(win, bg="#23272e")
        btn_frame.grid(row=6, column=0, sticky="ew", padx=32, pady=(0, 28))
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        if save_callback:
            tk.Button(btn_frame, text="저장", font=("맑은 고딕", 16, "bold"),
                      bg="#192a56", fg="#fbc531", height=2, relief=tk.FLAT,
                      activebackground="#273c75", activeforeground="#fbc531",
                      command=lambda: save_callback(
                          title_var.get(),
                          content_text.get("1.0", tk.END).strip(),
                          writer_var.get(), win)
                      ).grid(row=0, column=0, padx=10, sticky="ew")

        if delete_callback and post:
            tk.Button(btn_frame, text="삭제", font=("맑은 고딕", 16, "bold"),
                      bg="#c23616", fg="white", height=2, relief=tk.FLAT,
                      activebackground="#e84118", activeforeground="#fff",
                      command=lambda: delete_callback(win)
                      ).grid(row=0, column=1, padx=10, sticky="ew")

        tk.Button(btn_frame, text="닫기", font=("맑은 고딕", 16, "bold"),
                  bg="#353b48", fg="#00a8ff", height=2, relief=tk.FLAT,
                  activebackground="#2f3640", activeforeground="#00a8ff",
                  command=win.destroy
                  ).grid(row=0, column=2, padx=10, sticky="ew")

        # 단축키(Ctrl+S 저장 / Esc 닫기)
        if save_callback:
            win.bind("<Control-s>", lambda e: save_callback(
                title_var.get(),
                content_text.get("1.0", tk.END).strip(),
                writer_var.get(), win))
        win.bind("<Escape>", lambda e: win.destroy())

        # 포커스 + 중앙 배치
        title_entry.focus_set()
        win.update_idletasks()
        w = win.winfo_width()
        h = win.winfo_height()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        win.geometry(f"{w}x{h}+{(sw - w)//2}+{(sh - h)//2}")

# 실행
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = BoardApp(root)
    root.mainloop()

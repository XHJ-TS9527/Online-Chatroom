import tkinter as tk
from tkinter import messagebox
import threading


class register_win():

    def __init__(self, master, core):
        self.master = master
        self.core = core

    def init_win(self):
        self.window = tk.Toplevel()
        self.window.title('注册账号')
        self.window.geometry('330x160')
        self.window.resizable(0, 0)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.nickname_label = tk.Label(self.window, text='昵称: ')
        self.nickname_label.grid(row=0, column=0, padx=10, pady=10)
        self.nickname_textbox = tk.Entry(self.window)
        self.nickname_textbox.grid(row=0, column=1, padx=10, pady=10)
        self.password_label = tk.Label(self.window, text='密码: ')
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_textbox = tk.Entry(self.window)
        self.password_textbox.grid(row=1, column=1, padx=10, pady=10)
        self.register_button = tk.Button(self.window, text='注册', width=6, command=self.register)
        self.register_button.grid(row=3, column=0, columnspan=2)
        self.master.withdraw()

    def close_window(self):
        self.window.destroy()
        self.master.update()
        self.master.deiconify()

    def register(self):
        self.nickname = self.nickname_textbox.get()
        self.password = self.password_textbox.get()
        if len(self.password):
            self.register_threading = threading.Thread(target=self.register_thread)
            self.register_threading.setDaemon(True)
            self.register_threading.start()
        else:
            messagebox.showwarning('警告','密码不能为空')

    def register_thread(self):
        status, user_id = self.core.register_user(self.nickname, self.password)
        if status == 1:
            messagebox.showinfo('提示', '注册成功,您的账号是【%s】,请牢记!' % user_id)
            self.close_window()
        elif status == 0:
            messagebox.showerror('提示', '注册失败,请稍后重试')
        else:
            messagebox.showerror('网络中断','网络中断,请连接网络后重新尝试')
            self.close_window()

import tkinter as tk
from tkinter import messagebox
import threading
import time

import register_window as register_window
import main_window as main_window
import global_manager as gm

class login_win():

    def __init__(self, core):
        self.core = core
        self.stop_flag = 0

    def initwin(self):
        self.window = tk.Tk()
        self.window.title('Linux网络聊天室')
        #self.window.geometry('330x160')
        self.window.resizable(0, 0)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.account_label = tk.Label(self.window, text='账号: ')
        self.account_label.grid(row=0, column=0, padx=10, pady=10)
        self.account_textbox = tk.Entry(self.window)
        self.account_textbox.grid(row=0, column=1, padx=10, pady=10)
        self.password_label = tk.Label(self.window, text='密码: ')
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_textbox = tk.Entry(self.window)
        self.password_textbox.grid(row=1, column=1, padx=10, pady=10)
        self.register_button = tk.Button(self.window, text='注册', width=6, command=self.register)
        self.register_button.grid(row = 3, column=0, padx=10, pady=10, sticky=tk.W)
        self.login_button = tk.Button(self.window, text='登录', width=6, command=self.login)
        self.login_button.grid(row=3, column=1, padx=10, pady=10, sticky=tk.E)
        self.network_thread = threading.Thread(target=self.connect_network)
        self.network_thread.setDaemon(True)
        self.network_thread.start()
        self.window.mainloop()

    def close_window(self):
        res = messagebox.askokcancel('提示', '是否关闭窗口')
        if res:
            self.stop_flag = 1
            gm.set_global_var('stop flag', 1)
            self.window.destroy()

    def register(self):
        register_win = register_window.register_win(self.window, self.core)
        register_win.init_win()

    def login(self):
        self.account = self.account_textbox.get()
        self.password = self.password_textbox.get()
        if len(self.password):
            self.login_threading = threading.Thread(target=self.login_thread)
            self.login_threading.setDaemon(True)
            self.login_threading.start()
        else:
            messagebox.showwarning('警告', '密码不能为空')

    def login_thread(self):
        status, nickname = self.core.login(self.account, self.password)
        if status == 1:
            self.main_window = main_window.main_win(self.window, self.core, self.account)
            self.main_window.initwin()
        elif status == -1:
            messagebox.showwarning('提示', '密码错误')
        elif status == 0:
            messagebox.showerror('提示', '登录失败,请稍后重试')
        else:
            messagebox.showerror('网络中断','网络中断,请连接网络后重新尝试')

    def connect_network(self):
        while 1:
            if self.stop_flag:
                break
            if gm.get_global_var('connection broken'):
                self.core.connect()
                time.sleep(0.5)

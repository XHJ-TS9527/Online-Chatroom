import sys
sys.path.append('..')
import tkinter as tk
from tkinter import messagebox

import global_manager as gm


class change_password_win():

    def __init__(self, master):
        self.master = master

    def initwin(self):
        self.window = tk.Toplevel()
        self.window.title('修改密码')
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.columnconfigure(0, weight=1)
        self.label = tk.Label(self.window, text='请输入新密码: ')
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.entrybox = tk.Entry(self.window, width=35)
        self.entrybox.grid(row=0, column=1, padx=10, pady=10)
        self.button = tk.Button(self.window, text='提交', command=self.submit_change)
        self.button.grid(row=0, column=2, padx=10, pady=10)
        
    def submit_change(self):
        to_change_password = self.entrybox.get()
        if len(to_change_password):
            status = self.master.core.change_password(to_change_password)
            if status == 1:
                messagebox.showinfo('提示', '修改成功')
                self.master.window.update_idletasks()
                self.close_window()
            elif status == 0:
                messagebox.showerror('提示', '修改失败,请稍后重试')
            else:
                messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
                self.master.try_logout()
        else:
            messagebox.showerror('提示', '密码不能为空')

    def close_window(self):
        gm.set_global_var('change password window', 0)
        self.window.destroy()

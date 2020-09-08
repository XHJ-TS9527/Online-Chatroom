import sys
sys.path.append('..')
import tkinter as tk
from tkinter import messagebox

import global_manager as gm


class join_group_win():

    def __init__(self, master):
        self.master = master

    def initwin(self):
        self.window = tk.Toplevel()
        self.window.title('加入群组')
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.columnconfigure(0, weight=1)
        self.label = tk.Label(self.window, text='请输入需要加入的群号: ')
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.entrybox = tk.Entry(self.window, width=55)
        self.entrybox.grid(row=0, column=1, padx=10, pady=10)
        self.button = tk.Button(self.window, text='加入', command=self.submit_join)
        self.button.grid(row=0, column=2, padx=10, pady=10)

    def submit_join(self):
        to_join_group = self.entrybox.get()
        if len(to_join_group):
            if len(to_join_group) != 50 or not to_join_group.isnumeric():
                messagebox.showwarning('提示', '群号应为50位数字')
            else:
                status = self.master.core.join_group(to_join_group)
                if status == 1:
                    messagebox.showinfo('提示', '加入成功')
                elif status == 0:
                    messagebox.showerror('提示', '加入失败,请稍后重试')
                elif status == -1:
                    messagebox.showerror('提示', '该群不存在')
                else:
                    messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
                    self.master.try_logout()
        else:
            messagebox.showinfo('提示', '您没有输入需要加入的群组')

    def close_window(self):
        gm.set_global_var('join group window', 0)
        self.window.destroy()

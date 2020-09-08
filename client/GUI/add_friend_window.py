import sys
sys.path.append('..')
import tkinter as tk
from tkinter import messagebox

import global_manager as gm


class add_friend_win():

    def __init__(self, master):
        self.master = master

    def initwin(self):
        self.window = tk.Toplevel()
        self.window.title('添加好友')
        #self.window.geometry('200x300')
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.columnconfigure(0, weight=1)
        self.textlabel1 = tk.Label(self.window, text='需要添加的好友账号列表:')
        self.textlabel1.grid(row=0, column=0, columnspan=4, pady=10, sticky=tk.W)
        self.listbox = tk.Listbox(self.window, width=20, selectmode=tk.BROWSE)
        self.listbox.grid(row=1, column=0, columnspan=5, sticky=tk.NSEW)
        self.xscrollbar = tk.Scrollbar(self.window, command=self.listbox.xview, orient=tk.HORIZONTAL)
        self.xscrollbar.grid(row=2, column=0, columnspan=5,  sticky=tk.EW)
        self.yscrollbar = tk.Scrollbar(self.window, command=self.listbox.yview, orient=tk.VERTICAL)
        self.yscrollbar.grid(row=1, column=5, sticky=tk.NS)
        self.listbox.config(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)
        self.textlabel2 = tk.Label(self.window, text='添加账号: ')
        self.textlabel2.grid(row=3, column=0, padx=5, pady=10)
        self.entrybox = tk.Entry(self.window, width=15)
        self.entrybox.grid(row=3, column=1, padx=5, pady=10)
        self.sure_button = tk.Button(self.window, text='添加', width=5, command=self.insert_account)
        self.sure_button.grid(row=3, column=2, padx=5, pady=10)
        self.remove_button = tk.Button(self.window, text='移除', width=5, command=self.delete_account)
        self.remove_button.grid(row=3, column=3, padx=5, pady=10)
        self.confirm_button = tk.Button(self.window, text='发送', width=5, command=self.send_requests)
        self.confirm_button.grid(row=3, column=4, columnspan=2, padx=10, pady=10)

    def insert_account(self):
        to_add_account = self.entrybox.get()
        if len(to_add_account) != 13 or not to_add_account.isnumeric():
            messagebox.showwarning('提示','用户账号应为13位数字')
        elif to_add_account == self.master.id:
            messagebox.showwarning('提示', '您不能添加自己为好友.')
        else:
            self.listbox.insert(tk.END, to_add_account)
            self.entrybox.delete(0, tk.END)
            self.window.update_idletasks()

    def delete_account(self):
        self.listbox.delete(tk.ACTIVE)

    def send_requests(self):
        to_send_friends = self.listbox.get(0, tk.END)
        if len(to_send_friends):
            status = self.master.core.add_friend_request(to_send_friends)
            if status == 1:
                messagebox.showinfo('提示','好友请求发送成功')
                self.close_window()
            elif status == 0:
                messagebox.showerror('提示','好友请求发送失败,请稍后重试')
            else:
                messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
                self.master.try_logout()
        else:
            messagebox.showinfo('提示','您没有添加任何人为好友')
            self.close_window()

    def close_window(self):
        gm.set_global_var('add friend window', 0)
        self.window.destroy()

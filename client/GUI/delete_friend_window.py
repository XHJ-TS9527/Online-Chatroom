import sys
sys.path.append('..')
import tkinter as tk
from tkinter import messagebox

import global_manager as gm


class delete_friend_win():

    def __init__(self, master):
        self.master = master

    def initwin(self):
        self.window = tk.Toplevel()
        self.window.title('删除好友')
        self.window.geometry('300x350')
        self.window.protocol('WM_DELETE_WINDOW', self.direct_close_window)
        self.window.columnconfigure(0, weight=1)
        self.label = tk.Label(self.window, text='请选择你需要删除的好友:')
        self.label.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)
        self.listbox = tk.Listbox(self.window, width=50, selectmode=tk.MULTIPLE)
        self.listbox.grid(row=1, column=0, sticky=tk.NSEW)
        self.xscrollbar = tk.Scrollbar(self.window, command=self.listbox.xview, orient=tk.HORIZONTAL)
        self.xscrollbar.grid(row=2, column=0, sticky=tk.EW)
        self.yscrollbar = tk.Scrollbar(self.window, command=self.listbox.yview, orient=tk.VERTICAL)
        self.yscrollbar.grid(row=1, column=1, sticky=tk.NS)
        self.submit_button = tk.Button(self.window, width=15, text='提交好友删除请求', command=self.delete_friend_request)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def refresh_content(self, content):
        self.listbox.delete(0, tk.END)
        for each in content:
            self.listbox.insert(tk.END, '%s 【%s】' % (each['user_nickname'], each['user_id']))
        self.window.update_idletasks()

    def delete_friend_request(self):
        if len(self.listbox.curselection()):
            selection = self.listbox.curselection()
            listbox_content = self.listbox.get(0, tk.END)
            delete_friend_ids = []
            for each_selection in selection:
                each = listbox_content[each_selection]
                temp_string = each.split('【')
                temp_string = temp_string[1]
                temp_string = temp_string.split('】')
                delete_friend_ids.append(temp_string[0])
            status = self.master.core.delete_friends(delete_friend_ids)
            if status == 1:
                messagebox.showinfo('提示', '好友删除成功')
                self.direct_close_window()
            elif status == 0:
                messagebox.showerror('提示', '好友删除失败,请稍后重试')
            else:
                messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
                self.master.try_logout()
        else:
            messagebox.showinfo('提示', '您没有删除任何好友')
            self.direct_close_window()

    def direct_close_window(self):
        gm.set_global_var('delete friend window', 0)
        self.window.destroy()

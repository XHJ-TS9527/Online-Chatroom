import sys
sys.path.append('..')
import tkinter as tk
from tkinter import messagebox

import global_manager as gm


class cope_friend_win():

    def __init__(self, master):
        self.master = master

    def initwin(self):
        gm.set_global_var('cope_friend_close_msgbox', 0)
        self.window = tk.Toplevel()
        self.window.title('处理好友请求')
        self.window.geometry('300x350')
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.columnconfigure(0, weight=1)
        self.label = tk.Label(self.window, text='请选择你需要同意的好友请求:')
        self.label.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)
        self.listbox = tk.Listbox(self.window, width=50, selectmode=tk.MULTIPLE)
        self.listbox.grid(row=1, column=0, sticky=tk.NSEW)
        self.xscrollbar = tk.Scrollbar(self.window, command=self.listbox.xview, orient=tk.HORIZONTAL)
        self.xscrollbar.grid(row=2, column=0, sticky=tk.EW)
        self.yscrollbar = tk.Scrollbar(self.window, command=self.listbox.yview, orient=tk.VERTICAL)
        self.yscrollbar.grid(row=1, column=1, sticky=tk.NS)
        self.submit_button = tk.Button(self.window, width=15, text='提交好友添加请求', command=self.submit_friend_request)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def refresh_content(self, content):
        self.listbox.delete(0, tk.END)
        for each in content:
            self.listbox.insert(tk.END, '%s 【%s】' % (each['user_name'], each['user_id']))
        self.window.update_idletasks()

    def submit_friend_request(self):
        selection = self.listbox.curselection()
        listbox_content = self.listbox.get(0, tk.END)
        if len(selection):
            add_friend_ids = []
            for each_selection in selection:
                each = listbox_content[each_selection]
                temp_string = each.split('【')
                temp_string = temp_string[1]
                temp_string = temp_string.split('】')
                add_friend_ids.append(temp_string[0])
            status = self.master.core.add_friends(add_friend_ids)
            if status == 1:
                messagebox.showinfo('提示', '好友通过请求发送成功')
                self.direct_close_window()
            elif status == 0:
                messagebox.showerror('提示', '好友通过请求发送失败,请稍后重试')
            else:
                messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
                self.master.try_logout()
        else:
            messagebox.showinfo('提示', '您没有通过任何好友请求')
            self.direct_close_window()

    def direct_close_window(self):
        gm.set_global_var('cope friend window', 0)
        self.window.destroy()

    def close_window(self):
        if not gm.get_global_var('cope_friend_close_msgbox'):
            gm.set_global_var('cope_friend_close_msgbox', 1)
            res = messagebox.askyesno('提示', '您还没有处理当前的好友请求,离开时好友请求将全部丢失,是否继续?')
            if res:
                self.direct_close_window()
            else:
                gm.set_global_var('cope_friend_close_msgbox', 0)

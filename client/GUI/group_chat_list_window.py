import sys
sys.path.append('..')
import tkinter as tk
from tkinter import messagebox

import global_manager as gm
import chat_window as chat_window


class group_chat_list_win():

    def __init__(self, master):
        self.master = master
        self.chat_cnt = 0

    def initwin(self):
        self.window = tk.Toplevel()
        self.window.title('群聊')
        self.window.geometry('800x350')
        self.window.protocol('WM_DELETE_WINDOW', self.direct_close_window)
        self.window.columnconfigure(0, weight=1)
        self.label = tk.Label(self.window, text='请选择你需要参与的群聊:')
        self.label.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)
        self.listbox = tk.Listbox(self.window, width=50, selectmode=tk.BROWSE)
        self.listbox.grid(row=1, column=0, sticky=tk.NSEW)
        self.xscrollbar = tk.Scrollbar(self.window, command=self.listbox.xview, orient=tk.HORIZONTAL)
        self.xscrollbar.grid(row=2, column=0, sticky=tk.EW)
        self.yscrollbar = tk.Scrollbar(self.window, command=self.listbox.yview, orient=tk.VERTICAL)
        self.yscrollbar.grid(row=1, column=1, sticky=tk.NS)
        self.submit_button = tk.Button(self.window, width=15, text='参与群聊', command=self.new_chat)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def new_chat(self):
        if len(self.listbox.curselection()):
            selection = self.listbox.curselection()[0]
            listbox_content = self.listbox.get(0, tk.END)
            selection = listbox_content[selection]
            temp_string = selection.split(':')
            target_id = temp_string[0]
            new_window = chat_window.chat_win(self, 1, target_id, self.chat_cnt, selection)
            new_window.initwin()
            gm.append_global_var_list_item('group chat windows', new_window)
            self.chat_cnt += 1
            listbox_content = list(self.listbox.get(0, tk.END))
            listbox_content.remove(selection)
            self.listbox.delete(0, tk.END)
            for each in listbox_content:
                self.listbox.insert(tk.END, each)
        else:
            messagebox.showwarning('提示', '请选择一个群参与群聊')

    def refresh_content(self, content):
        self.listbox.delete(0, tk.END)
        for each in content:
            group_content = []
            for each_member in each['group_members']:
                group_content.append(each_member[1])
            self.listbox.insert(tk.END, '%s:%s' % (each['group_id'], ','.join(group_content)))
        self.window.update_idletasks()

    def direct_close_window(self):
        if len(gm.get_global_var('group chat windows')):
            res = messagebox.askokcancel('提示', '您当前还有正在进行的聊天,确定要结束吗')
            if res:
                while len(gm.get_global_var('group chat windows')):
                    this_window = gm.get_global_var('group chat windows')[0]
                    this_window.close_window()
                gm.set_global_var('group chat window', 0)
                self.window.destroy()
        else:
            gm.set_global_var('group chat window', 0)
            self.window.destroy()

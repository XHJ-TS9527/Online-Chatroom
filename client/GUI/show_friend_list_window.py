import sys
sys.path.append('..')
import tkinter as tk

import global_manager as gm

class show_friend_list_win():

    def __init__(self, master):
        self.master = master

    def initwin(self):
        self.window = tk.Toplevel()
        self.window.title('好友列表')
        self.window.geometry('300x300')
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.columnconfigure(0, weight=1)
        self.listbox = tk.Listbox(self.window, width=50)
        self.listbox.grid(row=0, column=0, sticky=tk.NSEW)
        self.xscrollbar = tk.Scrollbar(self.window, command=self.listbox.xview, orient=tk.HORIZONTAL)
        self.xscrollbar.grid(row=1, column=0, sticky=tk.EW)
        self.yscrollbar = tk.Scrollbar(self.window, command=self.listbox.yview, orient=tk.VERTICAL)
        self.yscrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.listbox.config(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)

    def refresh_content(self, content):
        self.listbox.delete(0, tk.END)
        for each_friend in content:
            self.listbox.insert(tk.END, '%s:\t%s' % (each_friend['user_id'], each_friend['user_nickname']))
        self.window.update_idletasks()

    def close_window(self):
        gm.set_global_var('show friend window', 0)
        self.window.destroy()

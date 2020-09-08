import sys
sys.path.append('..')
import tkinter as tk
from tkinter import ttk

import global_manager as gm

class show_group_list_win():

    def __init__(self, master):
        self.master = master

    def initwin(self):
        self.window = tk.Toplevel()
        self.window.title('群组列表')
        self.window.geometry('800x270')
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.columnconfigure(0, weight=1)
        columns = ('group')
        self.treeview = ttk.Treeview(self.window, columns=columns, selectmode=tk.BROWSE)
        self.treeview.heading('#0', text='用户账号')
        self.treeview.column('#0',anchor=tk.CENTER,width=550)
        self.treeview.heading('#1', text='用户昵称')
        self.treeview.column('#1',anchor=tk.CENTER,width=250)
        self.treeview.grid(row=0, column=0, sticky=tk.NSEW)
        self.xscrollbar = tk.Scrollbar(self.window, command=self.treeview.xview, orient=tk.HORIZONTAL)
        self.xscrollbar.grid(row=1, column=0, sticky=tk.EW)
        self.yscrollbar = tk.Scrollbar(self.window, command=self.treeview.yview, orient=tk.VERTICAL)
        self.yscrollbar.grid(row=0, column=1, sticky=tk.NS)

    def refresh_content(self, content):
        old_items = self.treeview.get_children()
        self.treeview.tag_configure('evenColor',background='lightpink')
        self.treeview.tag_configure('groupColor',background='lawngreen')
        [self.treeview.delete(item) for item in old_items]
        group_cnt = 1
        group_branch_cnt = 1
        for each_group in content:
            group_id = each_group['group_id']
            group_members = each_group['group_members']
            group_node = self.treeview.insert('', tk.END, 'group_item%i' % group_cnt, text=group_id, tag=('groupColor'))
            group_cnt += 1
            row_cnt = 1
            for each_member in group_members:
                user_id = each_member[0]
                user_nickname = each_member[1]
                if row_cnt % 2:
                    self.treeview.insert(group_node, tk.END, 'member_item%i' % group_branch_cnt, text=user_id,
                                         values=user_nickname)
                else:
                    self.treeview.insert(group_node, tk.END, 'member_item%i' % group_branch_cnt, text=user_id,
                                         values=user_nickname, tag=('evenColor'))
                group_branch_cnt += 1
                row_cnt +=1
        self.window.update_idletasks()

    def close_window(self):
        gm.set_global_var('show group window', 0)
        self.window.destroy()

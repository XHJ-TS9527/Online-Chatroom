import sys
sys.path.append('..')
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import global_manager as gm


class quit_grouop_win():

    def __init__(self, master):
        self.master = master

    def initwin(self):
        self.window = tk.Toplevel()
        self.window.title('退出群聊')
        self.window.geometry('800x310')
        self.window.protocol('WM_DELETE_WINDOW', self.direct_close_window)
        self.window.columnconfigure(0, weight=1)
        self.label = tk.Label(self.window, text='请选择你需要退出的群聊:')
        self.label.grid(row=0, column=0, pady=10)
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
        self.submit_button = tk.Button(self.window, width=15, text='退出', command=self.quit_group_request)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def refresh_content(self, content):
        self.content = content
        old_items = self.treeview.get_children()
        [self.treeview.delete(item) for item in old_items]
        group_cnt = 1
        group_branch_cnt = 1
        self.treeview.tag_configure('evenColor', background='lightpink')
        self.treeview.tag_configure('groupColor', background='lawngreen')
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
                row_cnt += 1
        self.window.update_idletasks()

    def quit_group_request(self):
        selection = self.treeview.selection()[0]
        if len(selection):
            if 'member' in selection:
                messagebox.showerror('提示', '您需要选择一个群组而不是一个群成员')
            else:
                select_idx = int(selection.replace('group_item','')) - 1
                to_quit_group_id = self.content[select_idx]['group_id']
                status = self.master.core.quit_group(to_quit_group_id)
                if status == 1:
                    messagebox.showinfo('提示', '群组退出成功')
                    self.direct_close_window()
                elif status == 0:
                    messagebox.showerror('提示', '群组退出失败,请稍后重试')
                else:
                    messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
                    self.master.try_logout()
        else:
            messagebox.showerror('提示', '您没有选择任何一个群组')

    def direct_close_window(self):
        gm.set_global_var('quit group window', 0)
        self.window.destroy()

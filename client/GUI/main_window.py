import sys
sys.path.append('..')
import tkinter as tk
from tkinter import messagebox
import threading

import global_manager as gm
import show_friend_list_window as show_friend_list_window
import show_group_list_window as show_group_list_window
import add_friend_window as add_friend_window
import cope_friend_request_window as cope_friend_request_window
import delete_friend_window as delete_friend_window
import join_group_window as join_group_window
import quit_group_window as quit_group_window
import private_chat_list_window as private_chat_list_window
import group_chat_list_window as group_chat_list_window
import change_nickname_window as change_nickname_window
import change_password_window as change_password_window

class main_win():

    def __init__(self,master, core, usr_id):
        self.master = master
        self.core = core
        self.id = usr_id
        gm.set_global_var('show friend window', 0)
        gm.set_global_var('show group window', 0)
        gm.set_global_var('add friend window', 0)
        gm.set_global_var('cope friend window', 0)
        gm.set_global_var('delete friend window', 0)
        gm.set_global_var('join group window', 0)
        gm.set_global_var('quit group window', 0)
        gm.set_global_var('private chat window', 0)
        gm.set_global_var('private chat windows', [])
        gm.set_global_var('group chat window', 0)
        gm.set_global_var('group chat windows', [])
        gm.set_global_var('change nickname window', 0)
        gm.set_global_var('change password window', 0)
        gm.set_global_var('chatting id', '')

    def initwin(self):
        width = 15
        self.window = tk.Toplevel()
        self.window.title('Linux网络聊天室')
        #self.window.geometry('230x680')
        self.window.resizable(0, 0)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.nickname_var = tk.StringVar()
        self.nickname_var.set('您好,%s' % self.core.get_nickname())
        self.nickname_label = tk.Label(self.window, textvariable = self.nickname_var)
        self.nickname_label.grid(row = 0, column = 0, columnspan=3, padx=10, pady=5)
        self.show_friend_list_button = tk.Button(self.window, text="显示好友列表", width=width, command=self.show_friend_list)
        self.show_friend_list_button.grid(row=1, column=0, padx=10, pady=5)
        self.show_group_list_button = tk.Button(self.window, text='显示群聊列表', width=width, command=self.show_group_list)
        self.show_group_list_button.grid(row=1, column=1, padx=10, pady=5)
        self.add_friends_button = tk.Button(self.window, text='添加好友', width=width, command=self.add_friend)
        self.add_friends_button.grid(row=1, column=2, padx=10, pady=5)
        self.cope_friend_button = tk.Button(self.window, text='处理好友添加请求', width=width, command=self.cope_friend)
        self.cope_friend_button.grid(row=2, column=0, padx=10, pady=5)
        self.delete_friend_button = tk.Button(self.window, text='删除好友', width=width, command=self.delete_friend)
        self.delete_friend_button.grid(row=2, column=1, padx=10, pady=5)
        self.apply_group_button = tk.Button(self.window, text='申请创建群聊', width=width, command=self.apply_group)
        self.apply_group_button.grid(row=2, column=2, padx=10, pady=5)
        self.join_group_button = tk.Button(self.window, text='加入群聊', width=width, command=self.join_group)
        self.join_group_button.grid(row=3, column=0, padx=10, pady=5)
        self.quit_group_button = tk.Button(self.window, text='退出群聊', width=width, command=self.quit_group)
        self.quit_group_button.grid(row=3, column=1, padx=10, pady=5)
        self.private_chat_button = tk.Button(self.window, text='好友私聊', width=width, command=self.private_chat)
        self.private_chat_button.grid(row=3, column=2, padx=10, pady=5)
        self.group_chat_button = tk.Button(self.window, text='参与群聊', width=width, command=self.group_chat)
        self.group_chat_button.grid(row=4, column=0, padx=10, pady=5)
        self.change_nickname_button = tk.Button(self.window, text='修改昵称', width=width, command=self.change_nickname)
        self.change_nickname_button.grid(row=4, column=1, padx=10, pady=5)
        self.change_password_button = tk.Button(self.window, text='修改密码', width=width, command=self.change_password)
        self.change_password_button.grid(row=4, column=2, padx=10, pady=5)
        self.unregister_button = tk.Button(self.window, text='注销账户', width=width, command=self.unregister)
        self.unregister_button.grid(row=5, column=0, padx=10, pady=5)
        self.logout_button = tk.Button(self.window, text='登出', width=width, command=self.logout)
        self.logout_button.grid(row=5, column=2, padx=10, pady=5)
        self.master.withdraw()

    def show_friend_list(self):
        self.show_friend_list_thread = threading.Thread(target=self.show_friend_list_core)
        self.show_friend_list_thread.setDaemon(True)
        self.show_friend_list_thread.start()

    def show_friend_list_core(self):
        if not gm.get_global_var('show friend window'):
            self.show_fried_window = show_friend_list_window.show_friend_list_win(self)
            self.show_fried_window.initwin()
            gm.set_global_var('show friend window', 1)
        status, friends = self.core.quest_friends_list()
        if status == 1:
            self.show_fried_window.refresh_content(friends)
            messagebox.showinfo('提示', '好友列表刷新成功')
        elif status == 0:
            messagebox.showinfo('提示', '好友列表请求失败,请稍后重试')
        else:
            messagebox.showerror('网络中断','网络中断,请连接网络后重新尝试')
            self.try_logout()

    def show_group_list(self):
        self.show_group_list_thread = threading.Thread(target=self.show_group_list_core)
        self.show_group_list_thread.setDaemon(True)
        self.show_group_list_thread.start()

    def show_group_list_core(self):
        if not gm.get_global_var('show group window'):
            self.show_group_window = show_group_list_window.show_group_list_win(self)
            self.show_group_window.initwin()
            gm.set_global_var('show group window', 1)
        status, groups = self.core.quest_group_list()
        if status == 1:
            self.show_group_window.refresh_content(groups)
            messagebox.showinfo('提示', '群聊列表刷新成功')
        elif status == 0:
            messagebox.showinfo('提示', '群聊列表请求失败,请稍后重试')
        else:
            messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
            self.try_logout()

    def add_friend(self):
        self.add_friend_thread = threading.Thread(target=self.add_friend_core)
        self.add_friend_thread.setDaemon(True)
        self.add_friend_thread.start()

    def add_friend_core(self):
        if not gm.get_global_var('add friend window'):
            self.add_friend_win = add_friend_window.add_friend_win(self)
            self.add_friend_win.initwin()
            gm.set_global_var('add friend window', 1)
        else:
            messagebox.showinfo('提示', '请在当前窗口完成好友添加')

    def cope_friend(self):
        self.cope_friend_thread = threading.Thread(target=self.cope_friend_core)
        self.cope_friend_thread.setDaemon(True)
        self.cope_friend_thread.start()

    def cope_friend_core(self):
        if not gm.get_global_var('cope friend window'):
            friend_requests = self.core.get_friend_request()
            if len(friend_requests):
                self.cope_friend_win = cope_friend_request_window.cope_friend_win(self)
                self.cope_friend_win.initwin()
                self.cope_friend_win.refresh_content(friend_requests)
                gm.set_global_var('cope friend window', 1)
            else:
                messagebox.showinfo('提示', '您当前没有好友请求')
        else:
            messagebox.showwarning('提示', '请先处理当前的好友请求')

    def delete_friend(self):
        self.delete_friend_thread = threading.Thread(target=self.delete_friend_core)
        self.delete_friend_thread.setDaemon(True)
        self.delete_friend_thread.start()

    def delete_friend_core(self):
        if not gm.get_global_var('delete friend window'):
            status, friend_list= self.core.quest_friends_list()
            if status == 1:
                if len(friend_list):
                    self.delete_friend_win = delete_friend_window.delete_friend_win(self)
                    self.delete_friend_win.initwin()
                    self.delete_friend_win.refresh_content(friend_list)
                    gm.set_global_var('delete friend window', 1)
                else:
                    messagebox.showinfo('提示', '您还没有任何好友')
            elif status == 0:
                messagebox.showerror('提示', '服务器处理错误,请稍后再试')
            else:
                messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
                self.try_logout()
        else:
            messagebox.showinfo('提示', '请在当前窗口完成好友删除')

    def apply_group(self):
        self.apply_group_thread = threading.Thread(target=self.apply_group_core)
        self.apply_group_thread.setDaemon(True)
        self.apply_group_thread.start()

    def apply_group_core(self):
        status, new_group_id = self.core.apply_new_group()
        if status == 1:
            messagebox.showinfo('提示', '新群申请成功,群号为【%s】,快邀请你的小伙伴们加入吧' % new_group_id)
        elif status == 0:
            messagebox.showerror('提示', '新群申请失败,请稍后再试')
        else:
            messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
            self.try_logout()

    def join_group(self):
        self.join_group_thread = threading.Thread(target=self.join_group_core)
        self.join_group_thread.setDaemon(True)
        self.join_group_thread.start()

    def join_group_core(self):
        if not gm.get_global_var('join group window'):
            self.join_group_win = join_group_window.join_group_win(self)
            self.join_group_win.initwin()
            gm.set_global_var('join group window', 1)
        else:
            messagebox.showinfo('提示', '请在当前窗口内完成加群')

    def quit_group(self):
        self.quit_group_thread = threading.Thread(target=self.quit_group_core)
        self.quit_group_thread.setDaemon(True)
        self.quit_group_thread.start()

    def quit_group_core(self):
        if not gm.get_global_var('quit group window'):
            status, groups = self.core.quest_group_list()
            if status == 1:
                if len(groups):
                    self.quit_group_win = quit_group_window.quit_grouop_win(self)
                    self.quit_group_win.initwin()
                    self.quit_group_win.refresh_content(groups)
                    gm.set_global_var('quit group window', 1)
                else:
                    messagebox.showinfo('提示', '您还没有加入任何群组')
            elif status == 0:
                messagebox.showerror('提示', '群组列表请求失败,请稍后重试')
            else:
                messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
                self.try_logout()
        else:
            messagebox.showinfo('提示', '请在当前窗口内完成退群')

    def private_chat(self):
        self.private_chat_thread = threading.Thread(target=self.private_chat_core)
        self.private_chat_thread.setDaemon(True)
        self.private_chat_thread.start()

    def private_chat_core(self):
        if not gm.get_global_var('private chat window'):
            status, friend_list = self.core.quest_friends_list()
            if status == 1:
                if len(friend_list):
                    self.private_chat_win = private_chat_list_window.private_chat_list_win(self)
                    self.private_chat_win.initwin()
                    self.private_chat_win.refresh_content(friend_list)
                    gm.set_global_var('private chat window', 1)
                else:
                    messagebox.showinfo('提示', '您还没有任何好友')
            elif status == 0:
                messagebox.showerror('提示', '服务器处理错误,请稍后再试')
            else:
                messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
                self.try_logout()
        else:
            messagebox.showinfo('提示', '请选择好友列表中的好友聊天')

    def group_chat(self):
        self.group_chat_thread = threading.Thread(target=self.group_chat_core)
        self.group_chat_thread.setDaemon(True)
        self.group_chat_thread.start()

    def group_chat_core(self):
        if not gm.get_global_var('group chat window'):
            status, group_list = self.core.quest_group_list()
            if status == 1:
                if len(group_list):
                    self.group_chat_win = group_chat_list_window.group_chat_list_win(self)
                    self.group_chat_win.initwin()
                    self.group_chat_win.refresh_content(group_list)
                    gm.set_global_var('group chat window', 1)
                else:
                    messagebox.showinfo('提示', '您没有加入任何群聊')
            elif status == 0:
                messagebox.showerror('提示', '服务器处理错误,请稍后再试')
            else:
                messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
                self.try_logout()
        else:
            messagebox.showinfo('提示', '请选择群组列表中的群组参与聊天')

    def change_nickname(self):
        self.change_nickname_thread = threading.Thread(target=self.change_nickname_core)
        self.change_nickname_thread.setDaemon(True)
        self.change_nickname_thread.start()

    def change_nickname_core(self):
        if not gm.get_global_var('change nickname window'):
            self.change_nickname_win = change_nickname_window.change_nickname_win(self)
            self.change_nickname_win.initwin()
            gm.set_global_var('change nickname window', 1)
        else:
            messagebox.showinfo('提示', '请在当前窗口内完成昵称更改')

    def change_password(self):
        self.change_password_thread = threading.Thread(target=self.change_password_core)
        self.change_password_thread.setDaemon(True)
        self.change_password_thread.start()

    def change_password_core(self):
        if not gm.get_global_var('change password window'):
            self.change_password_win = change_password_window.change_password_win(self)
            self.change_password_win.initwin()
            gm.set_global_var('change password window', 1)
        else:
            messagebox.showinfo('提示', '请在当前窗口内完成密码修改')

    def unregister(self):
        self.unregister_thread = threading.Thread(target=self.unregister_core)
        self.unregister_thread.setDaemon(True)
        self.unregister_thread.start()

    def unregister_core(self):
        status = self.core.unregister()
        if status == 1:
            messagebox.showinfo('提示','注销成功')
            self.try_logout()
        elif status == 0:
            messagebox.showerror('提示', '注销失败')

    def logout(self):
        self.logout_thread = threading.Thread(target=self.logout_core)
        self.logout_thread.setDaemon(True)
        self.logout_thread.start()

    def logout_core(self):
        status = self.core.logout()
        if status == 1:
            messagebox.showinfo('提示', '登出成功')
            self.direct_close_window()
        elif status == 0:
            messagebox.showerror('提示', '登出失败')
        else:
            messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
            self.direct_close_window()

    def try_logout(self):
        self.try_logout_thread = threading.Thread(target=self.try_logout_core)
        self.try_logout_thread.setDaemon(True)
        self.try_logout_thread.start()

    def try_logout_core(self):
        self.core.logout()
        self.direct_close_window()

    def direct_close_window(self):
        if gm.get_global_var('show friend window'):
            self.show_fried_window.close_window()
        if gm.get_global_var('show group window'):
            self.show_group_window.close_window()
        if gm.get_global_var('add friend window'):
            self.add_friend_win.close_window()
        if gm.get_global_var('cope friend window'):
            self.cope_friend_win.direct_close_window()
        if gm.get_global_var('delete friend window'):
            self.delete_friend_win.direct_close_window()
        if gm.get_global_var('join group window'):
            self.join_group_win.close_window()
        if gm.get_global_var('quit group window'):
            self.quit_group_win.direct_close_window()
        if gm.get_global_var('private chat window'):
            while len(gm.get_global_var('private chat windows')):
                this_window = gm.get_global_var('private chat windows')[0]
                this_window.close_window()
            self.private_chat_win.direct_close_window()
        if gm.get_global_var('group chat window'):
            while len(gm.get_global_var('group chat windows')):
                this_window = gm.get_global_var('group chat windows')[0]
                this_window.close_window()
            self.group_chat_win.direct_close_window()
        if gm.get_global_var('change nickname window'):
            self.change_nickname_win.close_window()
        if gm.get_global_var('change password window'):
            self.change_password_win.close_window()
        self.window.destroy()
        #self.master.update()
        self.master.deiconify()

    def close_window(self):
        res = messagebox.askokcancel('提示', '是否离开聊天室')
        if res:
            self.logout()

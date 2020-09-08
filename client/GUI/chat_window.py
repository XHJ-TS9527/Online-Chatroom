import sys
sys.path.append('..')
import time
import json
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import threading

import global_manager as gm
import cache_opreration as cache


class chat_win():

    def __init__(self, master, type, target_id, chat_number, item, nickname=None):
        self.master = master
        self.type = type
        self.target_id = target_id
        self.chat_number = chat_number
        self.item = item
        self.nickname = nickname
        self.stop_flag = 0
        self.refresh_flag = 1
        self.content_commute = []
        self.id = self.master.master.id
        self.send_inspect_thread_quit = 0
        self.receive_show_thread_quit = 0
        self.receive_info_thread_quit = 0
        self.send_flag = 0
        self.send_cache = ''
        self.cnt = 0
        self.content_dict = dict()
        self.count_dict = dict()
        self.condition_dict = dict()
        self.condition_inspect = dict()
        self.askwindow_close = 0

    def initwin(self):
        self.window = tk.Toplevel()
        if self.type: # group chat
            self.window.title('群组 %s 的聊天' % self.target_id)
        else:
            self.window.title('与%s【%s】的私聊' % (self.nickname, self.target_id))
        self.window.geometry('500x450')
        self.window.protocol('WM_DELETE_WINDOW', self.ask_close_window)
        self.window.columnconfigure(0, weight=1)
        self.showtext = ScrolledText(self.window, width=400, height=16)
        self.showtext.tag_configure('send_tag', foreground='purple')
        self.showtext.tag_configure('receive_tag', foreground='red')
        self.showtext.config(state=tk.DISABLED)
        self.showtext.insert(tk.INSERT, '\n', 'send_tag')
        self.showtext.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)
        self.entertext_label = tk.Label(self.window, text='请在下面输入需要发送的消息:')
        self.entertext_label.grid(row=1, column=0, columnspan=2, padx=10, sticky=tk.W)
        self.entertext = tk.Text(self.window, width=380, height=5)
        self.entertext.grid(row=2, column=0, padx=10, pady=10, stick=tk.NSEW)
        self.send_button = tk.Button(self.window, text='发送', width=10, command=self.send_command)
        self.send_button.grid(row=2, column=1, padx=10, pady=10)
        self.chat_start()

    def chat_start(self):
        self.send_info_threading = threading.Thread(target=self.send_info_thread)
        self.send_info_inspect_threading = threading.Thread(target=self.send_info_inspect_thread)
        self.network_inspect_threading = threading.Thread(target=self.inspect_network_thread)
        self.receive_info_threading = threading.Thread(target=self.receive_info_thread)
        self.receive_show_threading = threading.Thread(target=self.receive_show_thread)
        self.send_info_threading.setDaemon(True)
        self.send_info_inspect_threading.setDaemon(True)
        self.network_inspect_threading.setDaemon(True)
        self.receive_info_threading.setDaemon(True)
        self.receive_show_threading.setDaemon(True)
        self.send_info_threading.start()
        self.send_info_inspect_threading.start()
        self.network_inspect_threading.start()
        self.receive_info_threading.start()
        self.receive_show_threading.start()

    def send_command(self):
        content = self.entertext.get('1.0', tk.END)
        if len(content):
            self.send_cache = content
            self.entertext.delete('1.0', tk.END)
            self.send_flag = 1
        else:
            messagebox.showwarning('提示', '不能发送空消息')

    def inspect_network_thread(self):
        while 1:
            if self.stop_flag:
                break
            if gm.get_global_var('connection broken'):
                self.stop_flag = 1
                messagebox.showerror('网络中断', '网络中断,请连接网络后重新尝试')
                self.master.master.trylogout()
                break

    def send_info_thread(self):
        while 1:
            if self.stop_flag:
                break
            if self.send_flag:
                content = self.send_cache
                time_stamp = int(time.time())
                local_time = time.localtime(time_stamp)
                operation_date = '%.4d-%.2d-%.2d' % (local_time[0], local_time[1], local_time[2])
                operation_time = '%.2d:%.2d:%.2d' % (local_time[3], local_time[4], local_time[5])
                moment = '%s %s' % (operation_date, operation_time)
                if self.type:
                    to_send_list = [{'group_id': self.target_id, 'send_date': moment, 'message_type': 1, 'message': content}]
                    send_json = json.dumps({'msgtype': 'msg_send', 'index': (1, self.chat_number, self.cnt), 'list': to_send_list})
                else:
                    to_send_list = [
                        {'user2_id': self.target_id, 'send_date': moment, 'message_type': 0, 'message': content},
                        {'user2_id': self.id, 'send_date': moment, 'message_type': 0, 'message': content}]
                    send_json = json.dumps({'msgtype': 'msg_send', 'index': (0, self.chat_number, self.cnt), 'list': to_send_list})
                gm.append_global_var_list_item('network send cache', send_json)
                self.content_dict[self.cnt] = send_json
                self.condition_dict[self.cnt] = -1
                self.condition_inspect[self.cnt] = False
                self.count_dict[self.cnt] = 0
                self.cnt += 1
                self.send_flag = 0

    def send_info_inspect_thread(self):
        while 1:
            if self.stop_flag and False not in self.condition_inspect.values():
                self.send_inspect_thread_quit = 1
                break
            if self.type:
                response = gm.get_global_var('network receive cache')
                possible_validate = []
                for idx in range(len(response)):
                    if response[idx]['msgtype'] == 'msg_send_rec' and response[idx]['index'][0] == 1 \
                            and response[idx]['index'][1] == self.chat_number:
                        possible_validate.append(response[idx])
                if len(possible_validate):
                    for each in possible_validate:
                        gm.remove_global_var_list_item('network receive cache', each)
                        index = each['index'][2]
                        if each['state']:
                            self.condition_dict[index] = 1
                            self.condition_inspect[index] = True
                        else:
                            if self.count_dict[index] < gm.get_global_var('try times'):
                                gm.append_global_var_list_item('network send cache', self.content_dict[index])
                                self.count_dict[index] += 1
                            else:
                                this_send_content = json.loads(self.content_dict[index])['message']
                                while not self.refresh_flag:
                                    pass
                                self.content_commute.append({
                                    'user_id': '',
                                    'user_name': '系统',
                                    'send_date': '当前时刻',
                                    'message': '【系统消息】您的消息:%s 发送失败.' % this_send_content})
                                self.condition_dict[index] = 0
                                self.condition_inspect[index] = True
            else:
                response = gm.get_global_var('network receive cache')
                possible_validate = []
                for idx in range(len(response)):
                    if response[idx]['msgtype'] == 'msg_send_rec' and response[idx]['index'][0] == 0 and \
                        response[idx]['index'][1] == self.chat_number:
                        possible_validate.append(response[idx])
                if len(possible_validate):
                    for each in possible_validate:
                        gm.remove_global_var_list_item('network receive cache', each)
                        index = each['index'][2]
                        if each['state']:
                            while not self.refresh_flag:
                                pass
                            self.refresh_flag = 0
                            content = json.loads(self.content_dict[index])['list'][1]
                            self.content_commute = [[{'send_date': content['send_date'], 'message': content['message']}],()]
                            self.condition_dict[index] = 1
                            self.condition_inspect[index] = True
                        else:
                            if self.count_dict[index] < gm.get_global_var('try times'):
                                gm.append_global_var_list_item('network send cache', self.content_dict[index])
                                self.count_dict[index] += 1
                            else:
                                this_send_content = json.loads(self.content_dict[index])['message']
                                while not self.refresh_flag:
                                    pass
                                self.content_commute.append({
                                    'user_name': '系统',
                                    'send_date': '当前时刻',
                                    'messsage': '您的消息:%s 发送失败.' % this_send_content
                                })
                                self.condition_dict[index] = 0
                                self.condition_inspect[index] = True

    def receive_info_thread(self):
        while 1:
            if self.stop_flag:
                self.receive_info_thread_quit = 1
                break
            if self.refresh_flag:
                if self.type:
                    message = cache.get_from_cache({'group_ids': [self.target_id]})
                    if len(message):
                        print('cache message:')
                        print(message)
                        self.refresh_flag = 0
                        self.content_commute = message
                else:
                    message = cache.get_from_cache({'user_ids': [self.id]})
                    message = cache.get_from_cache({'user_ids': [self.target_id]})
                    if len(message):
                        message = ([], message)
                        self.refresh_flag = 0
                        self.content_commute = message

    def receive_show_thread(self):
        while 1:
            if self.stop_flag and self.refresh_flag:
                self.receive_show_thread_quit = 1
                break
            if not self.refresh_flag:
                self.showtext.config(state=tk.NORMAL)
                temp_content = self.content_commute
                self.content_commute = []
                if self.type:
                    for each_message in temp_content:
                        user_id = each_message['user_id']
                        user_nickname =each_message['user_name']
                        send_date = each_message['send_date']
                        this_message =each_message['message']
                        if user_id == self.id:
                            show_content = '你在 %s 说:\n%s\n' % (send_date, this_message)
                            self.showtext.insert(tk.INSERT, show_content, 'send_tag')
                            self.showtext.see(tk.END)
                        else:
                            show_content = '%s【%s】在 %s 说:\n%s\n\n' % (user_nickname, user_id, send_date, this_message)
                            self.showtext.insert(tk.INSERT, show_content, 'receive_tag')
                            self.showtext.see(tk.END)
                else:
                    for each_message in temp_content[0]:
                        send_date = each_message['send_date']
                        this_message = each_message['message']
                        show_content = '你在 %s 说:\n%s\n' % (send_date, this_message)
                        self.showtext.insert(tk.INSERT, show_content, 'send_tag')
                        self.showtext.see(tk.END)
                    for each_message in temp_content[1]:
                        user_nickname = each_message['user_name']
                        send_date = each_message['send_date']
                        this_message = each_message['message']
                        show_content = '%s【%s】在 %s 说:\n%s\n\n' % (user_nickname, self.target_id, send_date, this_message)
                        self.showtext.insert(tk.INSERT, show_content, 'receive_tag')
                        self.showtext.see(tk.END)
                        self.window.title('与%s【%s】的私聊' % (user_nickname, self.target_id))
                self.refresh_flag = 1
                self.showtext.config(state=tk.DISABLED)

    def close_window(self):
        self.stop_flag = 1
        while not self.receive_show_thread_quit or not self.receive_info_thread_quit or not self.send_inspect_thread_quit:
            pass
        if self.type:
            gm.remove_global_var_list_item('group chat windows', self)
        else:
            gm.remove_global_var_list_item('private chat windows', self)
        self.master.listbox.insert(tk.END, self.item)
        self.window.destroy()

    def ask_close_window(self):
        if not self.askwindow_close:
            res = messagebox.askyesno('提示', '您要关闭该聊天窗口吗?')
            if res:
                self.close_window()
            self.askwindow_close = 1
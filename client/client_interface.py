#coding:utf-8
import sys
sys.path.append('./GUI')
import threading
import time
import json

import global_manager as gm
import client_core as core
import cache_opreration as cache
import login_window as login_window

class client_main():

    def __init__(self):
        self.function_core = core.client()

    def __del__(self):
        try:
            del self.function_core
        except:
            pass

    def no_GUI(self):
        exit_flag = 0
        login_state = 0
        print('>欢迎使用网络聊天室系统.')
        while 1:
            try:
                if gm.get_global_var('connection broken'):
                    log_state = 0
                    print('>正在尝试连接到服务器,请稍后.')
                    status = self.function_core.connect()
                    if status:
                        print('>服务器连接成功.')
                    else:
                        raise Exception
                while 1:
                    if login_state:
                        print('您好,%s!请选择功能:' % self.usr_nickname)
                        print('>1:查看好友列表')
                        print('>2:查看群聊列表')
                        print('>3:添加好友')
                        print('>4:处理好友申请')
                        print('>5:删除好友')
                        print('>6:创建群聊')
                        print('>7:加入群聊')
                        print('>8:退出群聊')
                        print('>9:好友私聊')
                        print('>10:参与群聊')
                        print('>11:修改昵称')
                        print('>12:修改密码')
                        print('>13:注销账户')
                        print('>14:退出登录')
                        choice = input('您选择的功能是:')
                        while choice not in [str(idx) for idx in range(1,15)]:
                            print('输入有误,请重新输入.')
                            choice = input('您选择的功能是:')
                        if choice == '1':
                            status, friend_list = self.function_core.quest_friends_list()
                            if status == 1:
                                print('您的好友列表:')
                                print('账号\t昵称')
                                print('===============================')
                                for each_friend in friend_list:
                                    print('%s\t%s' % (each_friend['user_id'], each_friend['user_nickname']))
                            elif status == 0:
                                print('>查询过程发生错误.')
                            else:
                                raise Exception
                        elif choice == '2':
                            status, group_list = self.function_core.quest_group_list()
                            if status == 1:
                                print('您当前加入的群聊列表:')
                                print('群号\t[群员账号, 群员昵称]')
                                print('===============================')
                                for each_group in group_list:
                                    print('%s\t%s' % (each_group['group_id'], each_group['group_members']))
                            elif status == 0:
                                print('>查询过程发生错误.')
                            else:
                                raise Exception
                        elif choice == '3':
                            add_friends = []
                            while 1:
                                to_add_friend = input('>请输入需要添加好友的账号(输入#*@退出):')
                                if to_add_friend == '#*@':
                                    break
                                elif to_add_friend.isnumeric():
                                    add_friends.append(to_add_friend)
                                elif to_add_friend == self.id:
                                    print('>您不能添加自己为好友.')
                                else:
                                    print('>好友账号应当为数字.')
                            if len(add_friends):
                                status = self.function_core.add_friend_request(add_friends)
                                if status == 1:
                                    print('>好友请求发送成功.')
                                elif status == 0:
                                    print('>好友请求发送失败.')
                                else:
                                    raise Exception
                            else:
                                print('>您没有添加任何好友')
                        elif choice == '4':
                            accept_ids = []
                            request_list = self.function_core.get_friend_request()
                            if len(request_list):
                                for each in request_list:
                                    selection = input('%s【%s】请求添加您为好友,请问您拒绝[N]还是接受[Y]:' % (
                                        each['user_name'], each['user_id']))
                                    while selection not in ('Y', 'N'):
                                        print('>输入错误,请重新输入.')
                                        selection = input('%s【%s】请求添加您为好友,请问您拒绝[N]还是接受[Y]:' % (
                                            each['user_name'], each['user_id']))
                                    if selection == 'Y':
                                        accept_ids.append(each['user_id'])
                                status = self.function_core.add_friends(accept_ids)
                                if status == 1:
                                    print('>好友添加操作处理成功.')
                                elif status == 0:
                                    print('>好友添加操作处理失败.')
                                else:
                                    raise Exception
                            else:
                                print('>当前暂无好友请求.')
                        elif choice == '5':
                            to_delete_ids = []
                            while 1:
                                id = input('>请输入需要删除的好友账号(输入#*@结束):')
                                if id == '#*@':
                                    break
                                elif id.isnumeric():
                                    to_delete_ids.append(id)
                                else:
                                    print('>好友账号应当为数字.')
                            if len(to_delete_ids):
                                status = self.function_core.delete_friends(to_delete_ids)
                                if status == 1:
                                    print('>好友删除成功.')
                                elif status == 0:
                                    print('>好友删除失败.')
                                else:
                                    raise Exception
                            else:
                                print('>您没有删除任何好友.')
                        elif choice == '6':
                            status, group_id = self.function_core.apply_new_group()
                            if status == 1:
                                print('>新群申请成功,群号为【%s】,快叫你的小伙伴们入群吧!' % group_id)
                            elif status == 0:
                                print('>新群申请失败.')
                            else:
                                raise Exception
                        elif choice == '7':
                            target_group_id = input('>请输入需要加入的群号(返回输入#*@):')
                            while target_group_id != '#*@' and not target_group_id.isnumeric():
                                print('>输入有误,请重新输入.')
                                target_group_id = input('>请输入需要加入的群号(返回输入#*@):')
                            if target_group_id != '#*@':
                                #print('status')
                                status = self.function_core.join_group(target_group_id)
                                #print(status)
                                if status == 1:
                                    print('>加入成功.')
                                elif status == -1:
                                    print('>该群不存在.')
                                elif status == 0:
                                    print('>加入失败.')
                                else:
                                    raise Exception
                        elif choice == '8':
                            target_group_id = input('>请输入需要退出的群号(返回输入#*@):')
                            while target_group_id != '#*@' and not target_group_id.isnumeric():
                                print('>输入有误,请重新输入.')
                                target_group_id = input('>请输入需要加入的群号(返回输入#*@):')
                            if target_group_id != '#*@':
                                status = self.function_core.quit_group(target_group_id)
                                if status == 1:
                                    print('>退出成功.')
                                elif status == 0:
                                    print('>退出失败.')
                                else:
                                    raise Exception
                        elif choice == '9':
                            friend_id = input('>请输入好友账号(输入#*@退出):')
                            while friend_id != '@*#' and not friend_id.isnumeric():
                                print('>输入有误,请重新输入.')
                                friend_id = input('>请输入好友账号(输入#*@退出):')
                            if friend_id != '#*@':
                                status, now_friend_list = self.function_core.quest_friends_list()
                                if status == 1:
                                    friend_exist_flag = 0
                                    for idx in range(len(now_friend_list)):
                                        if friend_id == now_friend_list[idx]['user_id']:
                                            friend_exist_flag = 1
                                            break
                                    if friend_exist_flag:
                                        print('>开始与%s【%s】的私聊,发送空白信息退出.' % (now_friend_list[idx]['user_nickname'], now_friend_list[idx]['user_id']))
                                        self.chat_id = friend_id
                                        gm.set_global_var('chat quit flag', 0)
                                        self.chat_show_thread = threading.Thread(target=self.show_message_thread_no_GUI)
                                        self.chat_show_thread.setDaemon(True)
                                        self.chat_send_thread = threading.Thread(target=self.send_message_thread_no_GUI)
                                        self.chat_send_thread.setDaemon(True)
                                        self.chat_inspect_thread = threading.Thread(target=self.send_message_thread_inspect)
                                        self.chat_inspect_thread.setDaemon(True)
                                        self.chat_show_thread.start()
                                        self.chat_send_thread.start()
                                        self.chat_inspect_thread.start()
                                        while not gm.get_global_var('chat quit flag') or False in self.insepect_status.values():
                                            pass
                                        print('>聊天退出.')
                                    else:
                                        print('>该账号不是您的好友.')
                                elif status == 0:
                                    print('>开启聊天失败.')
                                else:
                                    raise Exception
                        elif choice == '10':
                            group_id = input('>请输入群号(输入#*@退出):')
                            while group_id != '@*#' and not group_id.isnumeric():
                                print('>输入有误,请重新输入.')
                                group_id = input('>请输入群号(输入#*@退出):')
                            if group_id != '#*@':
                                status, now_group_list = self.function_core.quest_group_list()
                                if status == 1:
                                    group_exist_flag = 0
                                    for idx in range(len(now_group_list)):
                                        if group_id == now_group_list[idx]['group_id']:
                                            group_exist_flag = 1
                                            break
                                    if group_exist_flag:
                                        print('开始参加群【%s】的聊天,发送空白消息退出.' % group_id)
                                        self.chat_id = group_id
                                        gm.set_global_var('chat quit flag', 0)
                                        self.chat_show_thread = threading.Thread(target=self.show_message_thread_no_GUI)
                                        self.chat_show_thread.setDaemon(True)
                                        self.chat_send_thread = threading.Thread(target=self.send_message_thread_no_GUI)
                                        self.chat_send_thread.setDaemon(True)
                                        self.chat_inspect_thread = threading.Thread(
                                            target=self.send_message_thread_inspect)
                                        self.chat_inspect_thread.setDaemon(True)
                                        self.chat_show_thread.start()
                                        self.chat_send_thread.start()
                                        self.chat_inspect_thread.start()
                                        while not gm.get_global_var('chat quit flag') or False in self.insepect_status.values():
                                            pass
                                        print('>聊天退出.')
                                    else:
                                        print('>您还未加入该群.')
                                elif status == 0:
                                    print('>开启聊天失败.')
                                else:
                                    raise Exception
                        elif choice == '11':
                            new_nickname = input('>请输入您的新昵称:')
                            status = self.function_core.change_nickname(new_nickname)
                            if status == 1:
                                self.usr_nickname = new_nickname
                                print('>修改成功.')
                            elif status == 0:
                                print('>修改失败.')
                            else:
                                raise Exception
                        elif choice == '12':
                            new_password = input('>请输入您的新密码:')
                            if len(new_password):
                                status = self.function_core.change_password(new_password)
                                if status == 1:
                                    print('>修改成功.')
                                elif status == 0:
                                    print('>修改失败.')
                                else:
                                    raise Exception
                            else:
                                print('>密码不能为空.')
                        elif choice == '13':
                            status = self.function_core.unregister()
                            if status:
                                print('>注销成功.')
                                login_state = 0
                            elif status == 0:
                                print('>注销失败.')
                            else:
                                raise Exception
                        else:
                            status = self.function_core.logout()
                            if status:
                                print('>登出成功.')
                                cache.save_cache(self.id)
                                login_state = 0
                            elif status == 0:
                                print('>登出失败.')
                            else:
                                raise Exception
                    else:
                        print('>请选择功能')
                        print('>1:注册账户')
                        print('>2:登录账户')
                        print('>3:退出系统')
                        choice = input('您的选择是:')
                        while choice not in ('1', '2', '3'):
                            print('输入有误,请重新输入.')
                            choice = input('您的选择是:')
                        if choice == '1':
                            nickname = input('>请输入昵称:')
                            password = input('>请输入密码:')
                            while not len(password):
                                print('>密码不能为空.')
                                password = input('>请输入密码:')
                            status, user_id = self.function_core.register_user(nickname, password)
                            if status == 1:
                                print('>注册成功. 您的账号是:%s,请牢记!' % user_id)
                            elif status == 0:
                                print('>注册失败.')
                            else:
                                raise Exception
                        elif choice == '2':
                            user_id = input('>请输入您的账号:')
                            password = input('>请输入您的密码:')
                            while not len(password):
                                print('>密码不能为空.')
                                password = input('>请输入您的密码:')
                            status, nickname = self.function_core.login(user_id, password)
                            if status == 1:
                                print('>登录成功.')
                                self.id = user_id
                                self.usr_nickname = nickname
                                #print('before load in interface:', gm.get_global_var('msg_list cache'))
                                cache.load_cache(user_id)
                                #print('after load in interface:', gm.get_global_var('msg_list cache'))
                                login_state = 1
                            elif status == -1:
                                print('>密码错误.')
                            elif status == 0:
                                print('>登录失败.')
                            else:
                                raise Exception
                        else:
                            exit_flag = 1
                            break
                    #print(gm.get_global_var('connection broken'))
                    #print(gm.get_global_var('network receive cache'))
            except Exception as e:
                print(e)
                #print(gm.get_global_var('connection broken'))
                #print(gm.get_global_var('network receive cache'))
                choice = input('>网络断开,是否尝试重新连接[Y/N]:')
                while choice not in ('Y', 'N'):
                    print('输入有误,请重新输入.')
                    choice = input('>网络断开,是否尝试重新连接[Y/N]:')
                if choice == 'N':
                    exit_flag = 1
                    break
            if exit_flag:
                gm.set_global_var('stop flag', 1)
                time.sleep(2)
                del self.function_core
                break
    
    def inspect_network_thread_no_GUI(self):
        while 1:
            if gm.get_global_var('chat quit flag'):
                break
            if gm.get_global_var('connection broken'):
                raise Exception
                break

    def show_message_thread_no_GUI(self):
        while 1:
            if gm.get_global_var('chat quit flag'):
                break
            if len(self.chat_id) == 13:
                messages = cache.get_from_cache({'user_ids': [self.id]})
                if len(messages):
                    #print(messages)
                    for each in messages:
                        print('你在%s说:\n%s\n' % (each['send_date'], each['message']))
                messages = cache.get_from_cache({'user_ids': [self.chat_id]})
                if len(messages):
                    #print(messages)
                    for each in messages:
                        print('%s【%s】在%s说:\n%s\n' % (each['user_name'], self.chat_id, each['send_date'], each['message']))
                
            else:
                messages = cache.get_from_cache({'group_ids': [self.chat_id]})
                if len(messages):
                    #print(messages)
                    for each in messages:
                        print('%s【%s】在%s说:\n%s\n' % (each['user_name'], each['user_id'], each['send_date'], each['message']))
            time.sleep(0.1)

    def send_message_thread_no_GUI(self):
        self.confirm_status = dict()
        self.insepect_status = dict()
        self.content = dict()
        self.retry_times = dict()
        if len(self.chat_id) == 13:
            while 1:
                message = input('>')
                if len(message):
                    # time now
                    time_stamp = int(time.time())
                    local_time = time.localtime(time_stamp)
                    operation_date = '%.4d-%.2d-%.2d' % (local_time[0], local_time[1], local_time[2])
                    operation_time = '%.2d:%.2d:%.2d' % (local_time[3], local_time[4], local_time[5])
                    moment = '%s %s' % (operation_date, operation_time)
                    # send the data
                    this_cnt = gm.get_global_var('privacy chat cnt')
                    gm.set_global_var('privacy chat cnt', this_cnt + 1)
                    to_send_list = [{'user2_id': self.chat_id, 'send_date': moment, 'message_type': 0, 'message': message},
                                    {'user2_id': self.id, 'send_date': moment, 'message_type': 0, 'message': message}]
                    send_json = json.dumps({'msgtype': 'msg_send', 'index': (0, this_cnt), 'list': to_send_list})
                    gm.append_global_var_list_item('network send cache', send_json)
                    self.content[this_cnt] = send_json
                    self.retry_times[this_cnt] = 0
                    self.confirm_status[this_cnt] = -1
                    self.insepect_status[this_cnt] = False
                else:
                    gm.set_global_var('chat quit flag', 1)
                    if False in self.insepect_status.values():
                        print('>当前正在发送消息.发送完毕后退出.')
                        while False in self.insepect_status.values():
                            pass
                    break
        else:
            while 1:
                message = input('>')
                if len(message):
                    # time now
                    time_stamp = int(time.time())
                    local_time = time.localtime(time_stamp)
                    operation_date = '%.4d-%.2d-%.2d' % (local_time[0], local_time[1], local_time[2])
                    operation_time = '%.2d:%.2d:%.2d' % (local_time[3], local_time[4], local_time[5])
                    moment = '%s %s' % (operation_date, operation_time)
                    # send the data
                    this_cnt = gm.get_global_var('group chat cnt')
                    gm.set_global_var('group chat cnt', this_cnt + 1)
                    to_send_list = [{'group_id': self.chat_id, 'send_date': moment, 'message_type': 1, 'message': message}]
                    send_json = json.dumps({'msgtype': 'msg_send', 'index': (1, this_cnt), 'list': to_send_list})
                    gm.append_global_var_list_item('network send cache', send_json)
                    self.content[this_cnt] = send_json
                    self.retry_times[this_cnt] = 0
                    self.confirm_status[this_cnt] = -1
                    self.insepect_status[this_cnt] = False
                else:
                    gm.set_global_var('chat quit flag', 1)
                    if False in self.insepect_status.values():
                        print('>当前正在发送消息.发送完毕后退出.')
                        while False in self.insepect_status.values():
                            pass
                    break

    def send_message_thread_inspect(self):
        while 1:
            if gm.get_global_var('chat quit flag') and False not in self.insepect_status.values():
                break
            if len(self.chat_id) == 13:
                response = gm.get_global_var('network receive cache')
                possible_validate = []
                for idx in range(len(response)):
                    if response[idx]['msgtype'] == 'msg_send_rec' and response[idx]['index'][0] == 0:
                        possible_validate.append(response[idx])
                if len(possible_validate):
                    for each in possible_validate:
                        gm.remove_global_var_list_item('network receive cache', each)
                        index = each['index'][1]
                        if each['state']:
                            self.confirm_status[index] = 1
                            self.insepect_status[index] = True
                        else:
                            if  self.retry_times[index] < gm.get_global_var('try times'):
                                gm.append_global_var_list_item('network send cache', self.content[index])
                                self.retry_times[index] += 1
                            else:
                                this_send_content = json.loads(self.content[index])['list'][0]['message']
                                print('>【系统消息】您的消息:%s 发送失败.' % this_send_content)
                                self.confirm_status[index] = 0
                                self.insepect_status[index] = True
            else:
                response = gm.get_global_var('network receive cache')
                possible_validate = []
                for idx in range(len(response)):
                    if response[idx]['msgtype'] == 'msg_send_rec' and response[idx]['index'][0] == 1:
                        possible_validate.append(response[idx])
                if len(possible_validate):
                    for each in possible_validate:
                        gm.remove_global_var_list_item('network receive cache', each)
                        index = each['index'][1]
                        if each['state']:
                            self.confirm_status[index] = 1
                            self.insepect_status[index] = True
                        else:
                            if self.retry_times[index] < gm.get_global_var('try times'):
                                gm.append_global_var_list_item('network send cache', self.content[index])
                                self.retry_times[index] += 1
                            else:
                                this_send_content = json.loads(self.content[index])['list'][0]['message']
                                print('>【系统消息】您的消息:%s 发送失败.' % this_send_content)
                                self.confirm_status[index] = 0
                                self.insepect_status[index] = True
            time.sleep(0.1)

    def have_GUI(self):
        self.loginwin = login_window.login_win(self.function_core)
        self.loginwin.initwin()

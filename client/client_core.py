import time
import json
import threading

import client.client_network_service as service
import client.global_manager as gm
import client.cache_opreration as cache

class client():

    def __init__(self):
        self.socket_service = service.network_tool()
        self.nickname = ''
        self.id = ''
        self.password = ''

    def connect(self):
        if gm.get_global_var('connection broken'):
            ok_flag = 0
            for cnt in range(gm.get_global_var('try times')):
                try:
                    self.network_communicate_thread = threading.Thread(target=self.socket_service.start_network)
                    self.network_communicate_thread.setDaemon(True)
                    self.network_communicate_thread.start()
                    time.sleep(1)
                    receive_message = gm.get_global_var('network receive cache')
                    if {'msgtype': 'connect_succeed'} in receive_message:
                        while {'msgtype': 'connect_succeed'} in gm.get_global_var('network receive cache'):
                            print(gm.get_global_var('network receive cache'))
                            gm.remove_global_var_list_item('network receive cache', {'msgtype': 'connect_succeed'})
                        ok_flag = 1
                        break
                    
                except:
                    pass
            if ok_flag:
                gm.set_global_var('connection broken', 0)
            return ok_flag

    def get_nickname(self):
        return self.nickname

    def register_user(self, user_nickname, user_password):
        """
        :param user_nickname: string
        :param user_password: string
        :return: (status, None/user_id)
        -1: password empty
        0: error
        1: ok
        9999: connection error
        """
        if len(user_password):
            send_json = json.dumps({'msgtype': 'register', 'user_nickname': user_nickname, 'password': user_password})
            gm.append_global_var_list_item('network send cache', send_json)
            cnt = 0
            while 1:
                ok_flag = 0
                receive_message = gm.get_global_var('network receive cache')
                for idx in range(len(receive_message)):
                    if receive_message[idx]['msgtype'] == 'register':
                        ok_flag = 1
                        break
                if ok_flag:
                    response = receive_message[idx]
                    gm.remove_global_var_list_item('network receive cache', response)
                    if response['state']:
                        return 1, response['user_id']
                    else:
                        if cnt < gm.get_global_var('try times'):
                            gm.append_global_var_list_item('network send cache', send_json)
                            cnt += 1
                        else:
                            return 0, None
                if gm.get_global_var('connection broken'):
                    return 9999, None
                time.sleep(0.1)
        else:
            return -1, None # password should not be empty

    def login(self, user_id, password):
        """
        :param user_id: string
        :param password: string
        :return: (status, None/nickname)
        status
        -1: password incorrect or password empty
        0: error
        1: pass
        9999: connection error
        """
        if len(password):
            send_json = json.dumps({'msgtype': "binding", "account": user_id, "password": password})
            gm.append_global_var_list_item('network send cache', send_json)
            cnt = 0
            while 1:
                ok_flag = 0
                receive_message = gm.get_global_var('network receive cache')
                for idx in range(len(receive_message)):
                    if receive_message[idx]['msgtype'] == 'bind_state':
                        ok_flag = 1
                        break
                if ok_flag:
                    response = receive_message[idx]
                    gm.remove_global_var_list_item('network receive cache', response)
                    if response['state'] == 0:
                        return 1, response['user_nickname']
                    elif response['state'] == 1:
                        return -1, None
                    else:
                        if cnt < gm.get_global_var('try times'):
                            gm.append_global_var_list_item('network send cache', send_json)
                            cnt += 1
                        else:
                            return 0, None
                if gm.get_global_var('connection broken'):
                    return 9999, None
                time.sleep(0.1)
        else:
            return -1, None

    def quest_friends_list(self):
        """
        :return: (status, None/list of dict of friend ids and nickname)
        status:
        0: error
        1: ok
        9999: connection error
        """
        send_json = json.dumps({'msgtype': 'get_friend_list'})
        gm.append_global_var_list_item('network send cache', send_json)
        cnt = 0
        while 1:
            ok_flag = 0
            receive_message = gm.get_global_var('network receive cache')
            for idx in range(len(receive_message)):
                if receive_message[idx]['msgtype'] == 'friend_list':
                    ok_flag = 1
                    break
            if ok_flag:
                response = receive_message[idx]
                gm.remove_global_var_list_item('network receive cache', response)
                if response['state']:
                    return 1, response['list']
                else:
                    if cnt < gm.get_global_var('try times'):
                        gm.append_global_var_list_item('network send cache', send_json)
                        cnt += 1
                    else:
                        return 0, None
            if gm.get_global_var('connection broken'):
                return 9999, None
            time.sleep(0.1)

    def quest_group_list(self):
        """
        :return: (status, list of dictionary of group ids)
        status:
        0: error
        1: ok
        9999: connection error
        """
        send_json = json.dumps({'msgtype': 'get_group_list'})
        gm.append_global_var_list_item('network send cache', send_json)
        cnt = 0
        while 1:
            ok_flag = 0
            receive_message = gm.get_global_var('network receive cache')
            for idx in range(len(receive_message)):
                if receive_message[idx]['msgtype'] == 'group_list':
                    ok_flag = 1
                    break
            if ok_flag:
                response = receive_message[idx]
                gm.remove_global_var_list_item('network receive cache', response)
                if response['state']:
                    return 1, response['list']
                else:
                    if cnt < gm.get_global_var('try times'):
                        gm.append_global_var_list_item('network send cache', send_json)
                        cnt += 1
                    else:
                        return 0, None
            if gm.get_global_var('connection broken'):
                return 9999, None
            time.sleep(0.1)

    def add_friend_request(self, target_user_ids):
        """
        :param target_user_ids: list/tuple/set of string
        :return:
        0: error
        1: success
        9999: connection error
        """
        # time now
        time_stamp = int(time.time())
        local_time = time.localtime(time_stamp)
        operation_date = '%.4d-%.2d-%.2d' % (local_time[0], local_time[1], local_time[2])
        operation_time = '%.2d:%.2d:%.2d' % (local_time[3], local_time[4], local_time[5])
        moment = '%s %s' % (operation_date, operation_time)
        # send request
        to_add_friend_list = []
        for each in target_user_ids:
            to_add_friend_list.append({'user2_id': each, 'message_type': 2})
        this_cnt = gm.get_global_var('friend request cnt')
        gm.set_global_var('friend request cnt', this_cnt + 1)
        send_json = json.dumps({'msgtype': 'msg_send', 'index': (2, this_cnt), 'send_date': moment, 'list': to_add_friend_list})
        gm.append_global_var_list_item('network send cache', send_json)
        cnt = 0
        while 1:
            ok_flag = 0
            receive_message = gm.get_global_var('network receive cache')
            for idx in range(len(receive_message)):
                if receive_message[idx]['msgtype'] == 'msg_send_rec' and receive_message[idx]['index'][0] == 2:
                    ok_flag = 1
                    break
            if ok_flag:
                response = receive_message[idx]
                gm.remove_global_var_list_item('network receive cache', response)
                if response['state']:
                    return 1
                else:
                    if cnt < gm.get_global_var('try times'):
                        gm.append_global_var_list_item('network send cache', send_json)
                        cnt += 1
                    else:
                        return 0
            if gm.get_global_var('connection broken'):
                return 9999
            time.sleep(0.1)

    def get_friend_request(self):
        """
        :return: list of dicts of friend requests
        """
        return cache.get_from_cache({'friend_request': 0})

    def add_friends(self, friend_ids):
        """
        :param friend_ids: list/tuple/set of strings
        :return:
        0: error
        1: success
        9999: connection error
        """
        # send messages
        friend_dict_list = []
        for each_friend_id in friend_ids:
            friend_dict_list.append({'user2_id': each_friend_id, 'message_type': 3})
        this_cnt = gm.get_global_var('friend add cnt')
        gm.set_global_var('friend add cnt', this_cnt + 1)
        send_json = json.dumps({'msgtype': 'msg_send', 'index': (3, this_cnt), 'list': friend_dict_list})
        gm.append_global_var_list_item('network send cache', send_json)
        cnt = 0
        while 1:
            ok_flag = 0
            receive_message = gm.get_global_var('network receive cache')
            for idx in range(len(receive_message)):
                if receive_message[idx]['msgtype'] == 'msg_send_rec' and receive_message[idx]['index'][0] == 3:
                    ok_flag = 1
                    break
            if ok_flag:
                response = receive_message[idx]
                gm.remove_global_var_list_item('network receive cache', response)
                if response['state']:
                    return 1
                else:
                    if cnt < gm.get_global_var('try times'):
                        gm.append_global_var_list_item('network send cache', send_json)
                        cnt += 1
                    else:
                        return 0
            if gm.get_global_var('connection broken'):
                return 9999
            time.sleep(0.1)

    def delete_friends(self, friend_ids):
        """
        :param friend_ids: list/tuple/set of strings
        :return:
        0: error
        1: success
        9999: connection error
        """
        # send messages
        friend_dict_list = []
        for each_friend_id in friend_ids:
            friend_dict_list.append({'user2_id': each_friend_id, 'message_type': 4})
        this_cnt = gm.get_global_var('friend delete cnt')
        gm.set_global_var('friend delete cnt', this_cnt + 1)
        send_json = json.dumps({'msgtype': 'msg_send', 'index': (4, this_cnt), 'list': friend_dict_list})
        gm.append_global_var_list_item('network send cache', send_json)
        cnt = 0
        while 1:
            ok_flag = 0
            receive_message = gm.get_global_var('network receive cache')
            for idx in range(len(receive_message)):
                if receive_message[idx]['msgtype'] == 'msg_send_rec' and receive_message[idx]['index'][0] == 4:
                    ok_flag = 1
                    break
            if ok_flag:
                response = receive_message[idx]
                gm.remove_global_var_list_item('network receive cache', response)
                if response['state']:
                    return 1
                else:
                    if cnt < gm.get_global_var('try times'):
                        gm.append_global_var_list_item('network send cache', send_json)
                        cnt += 1
                    else:
                        return 0
            if gm.get_global_var('connection broken'):
                return 9999
            time.sleep(0.1)

    def change_nickname(self,new_nickname):
        """
        :param new_nickname: string
        :return:
        0: error
        1: success
        9999: connection error
        """
        send_json = json.dumps({'msgtype': 'change_info', 'object': 'user_nickname', 'change_to': new_nickname})
        gm.append_global_var_list_item('network send cache', send_json)
        cnt = 0
        while 1:
            ok_flag = 0
            receive_message = gm.get_global_var('network receive cache')
            for idx in range(len(receive_message)):
                if receive_message[idx]['msgtype'] == 'change_info' and receive_message[idx]['object'] == 'user_nickname':
                    ok_flag = 1
                    break
            if ok_flag:
                response = receive_message[idx]
                gm.remove_global_var_list_item('network receive cache', response)
                if response['state']:
                    return 1
                else:
                    if cnt < gm.get_global_var('try times'):
                        gm.append_global_var_list_item('network send cache', send_json)
                        cnt += 1
                    else:
                        return 0
            if gm.get_global_var('connection broken'):
                return 9999
            time.sleep(0.1)

    def change_password(self,new_password):
        """
        :param new_nickname: string
        :return:
        0: error
        1: success
        9999: connection error
        """
        send_json = json.dumps({'msgtype': 'change_info', 'object': 'user_password', 'change_to': new_password})
        gm.append_global_var_list_item('network send cache', send_json)
        cnt = 0
        while 1:
            ok_flag = 0
            receive_message = gm.get_global_var('network receive cache')
            for idx in range(len(receive_message)):
                if receive_message[idx]['msgtype'] == 'change_info' and receive_message[idx]['object'] == 'user_password':
                    ok_flag = 1
                    break
            if ok_flag:
                response = receive_message[idx]
                gm.remove_global_var_list_item('network receive cache', response)
                if response['state']:
                    return 1
                else:
                    if cnt < gm.get_global_var('try times'):
                        gm.append_global_var_list_item('network send cache', send_json)
                        cnt += 1
                    else:
                        return 0
            if gm.get_global_var('connection broken'):
                return 9999
            time.sleep(0.1)

    def apply_new_group(self):
        """
        :return: (status, None/new group_id)
        status:
        0: error
        1: success
        9999: connection error
        """
        send_json = json.dumps({'msgtype': 'apply_group'})
        gm.append_global_var_list_item('network send cache', send_json)
        cnt = 0
        while 1:
            ok_flag = 0
            receive_message = gm.get_global_var('network receive cache')
            for idx in range(len(receive_message)):
                if receive_message[idx]['msgtype'] == 'apply_group_success':
                    ok_flag = 1
                    break
            if ok_flag:
                response = receive_message[idx]
                gm.remove_global_var_list_item('network receive cache', response)
                if response['state']:
                    return 1, response['group_id']
                else:
                    if cnt < gm.get_global_var('try times'):
                        gm.append_global_var_list_item('network send cache', send_json)
                        cnt += 1
                    else:
                        return 0, None
            if gm.get_global_var('connection broken'):
                return 9999, None
            time.sleep(0.1)

    def join_group(self, group_id):
        """
        :param group_id: string
        :return:
        -1: group does not exist
        0: error
        1: ok
        9999: connection error
        """
        send_json = json.dumps({'msgtype': 'join_group', 'group_id': group_id})
        gm.append_global_var_list_item('network send cache', send_json)
        cnt = 0
        while 1:
            ok_flag = 0
            receive_message = gm.get_global_var('network receive cache')
            for idx in range(len(receive_message)):
                if receive_message[idx]['msgtype'] == 'join_group_success':
                    ok_flag = 1
                    break
            if ok_flag:
                response = receive_message[idx]
                gm.remove_global_var_list_item('network receive cache', response)
                if response['state'] == 0:
                    return -1
                elif response['state'] == 1:
                    return 1
                else:
                    if cnt < gm.get_global_var('try times'):
                        gm.append_global_var_list_item('network send cache', send_json)
                        cnt += 1
                    else:
                        return 0
            if gm.get_global_var('connection broken'):
                return 9999
            time.sleep(0.1)

    def quit_group(self, group_id):
        """
        :param group_id: string
        :return:
        0: error
        1: ok
        9999: connection error
        """
        send_json = json.dumps({'msgtype': 'quit_group', 'group_id': group_id})
        gm.append_global_var_list_item('network send cache', send_json)
        cnt = 0
        while 1:
            ok_flag = 0
            receive_message = gm.get_global_var('network receive cache')
            for idx in range(len(receive_message)):
                if receive_message[idx]['msgtype'] == 'quit_group':
                    ok_flag = 1
                    break
            if ok_flag:
                response = receive_message[idx]
                gm.remove_global_var_list_item('network receive cache', response)
                if response['state']:
                    return 1
                else:
                    if cnt < gm.get_global_var('try times'):
                        gm.append_global_var_list_item('network send cache', send_json)
                        cnt += 1
                    else:
                        return 0
            if gm.get_global_var('connection broken'):
                return 9999
            time.sleep(0.1)

    def logout(self):
        """
        :return:
        0: error
        1: ok
        9999: connection error
        """
        send_json = json.dumps({'msgtype': 'logout'})
        gm.append_global_var_list_item('network send cache', send_json)
        cnt = 0
        while 1:
            ok_flag = 0
            receive_message = gm.get_global_var('network receive cache')
            for idx in range(len(receive_message)):
                if receive_message[idx]['msgtype'] == 'logout':
                    ok_flag = 1
                    break
            if ok_flag:
                response = receive_message[idx]
                gm.remove_global_var_list_item('network receive cache', response)
                if response['state']:
                    return 1
                else:
                    if cnt < gm.get_global_var('try times'):
                        gm.append_global_var_list_item('network send cache', send_json)
                        cnt += 1
                    else:
                        return 0
            if gm.get_global_var('connection broken'):
                return 9999
            time.sleep(0.1)

    def unregister(self):
        """
        :return:
        0: error
        1: ok
        9999: connection error
        """
        send_json = json.dumps({'msgtype': 'unregister'})
        gm.append_global_var_list_item('network send cache', send_json)
        cnt = 0
        while 1:
            ok_flag = 0
            receive_message = gm.get_global_var('network receive cache')
            for idx in range(len(receive_message)):
                if receive_message[idx]['msgtype'] == 'unregister':
                    ok_flag = 1
                    break
            if ok_flag:
                response = receive_message[idx]
                gm.remove_global_var_list_item('network receive cache', response)
                if response['state']:
                    return 1
                else:
                    if cnt < gm.get_global_var('try times'):
                        gm.append_global_var_list_item('network send cache', send_json)
                        cnt += 1
                    else:
                        return 0
            if gm.get_global_var('connection broken'):
                return 9999
            time.sleep(0.1)

    def __del__(self):
        try:
            self.socket_service.disconnect_server()
        except:
            pass

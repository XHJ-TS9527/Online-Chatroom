from db.user_db_operation import *
from db.messagebox_db_operation import *
from db.cross_db_operation import *
import global_manager as gm

import time
import json

# global var 'connection dict'

def init_base_func(self):
    self.user_id = None
    self.name = None


def LOGIN(self, request_dict):
    status = login(request_dict['account'], request_dict['password'])
    if (status == -1) or (status == -2):
        return {'msgtype':'bind_state',
                'state':1}
    elif status == 0:
        return {'msgtype':'bind_state',
                'state':2}
    self.user_id = request_dict['account']

    status, user_list = get_nickname([self.user_id])
    if status != 1:
        return {'msgtype': 'bind_state',
                'state': 2}
    self.name = user_list[self.user_id][1]

    print('\n', self.user_id, 'connect to me\n')
    # if the connection with the user_id has exist, disconnect it and join the new obj
    conn_dict = gm.get_global_var('connection dict')
    tmp = conn_dict.get(self.user_id)
    if tmp != None and tmp != self:
        tmp.close()
    conn_dict[self.user_id] = self
    # print('before reflash')
    msg_reflash(self)
    return {'msgtype':'bind_state',
            'state':0,
            'user_nickname':self.name}


def Register(self, request_dict):
    status, user_id = register_user({'nickname':request_dict['user_nickname'],
                                     'password':request_dict['password']})
    if status != 1:
        return {'msgtype':request_dict['msgtype'],
                'state': 0}
    return {'msgtype':request_dict['msgtype'],
            'state': 1,
            'user_id':user_id}


def logout(self, request_dict):
    conn_dict = gm.get_global_var('connection dict')
    for user_id in conn_dict:
        if conn_dict[user_id] == self:
            del conn_dict[user_id]
            break
    if self.user_id == None:
        self.user_id = ()
    print([self.request.connection.context.address] + [self.user_id], ' : client disconnect!')
    init_base_func(self)
    return {"msgtype":"logout",
            'state':1}


def unregister(self, request_dict):
    # this op need that self.user_id is not None
    if self.user_id == None:
        return {"msgtype": "logout",
                'state': 1}
    status = unregister_user(self.user_id)
    if status != 1:
        return {'msgtype': request_dict['msgtype'],
                'state':0}
    logout(self, request_dict)
    return {'msgtype': request_dict['msgtype'],
            'state':1}


def msg_reflash(self):
    # this op need that self.user_id is not None
    if self.user_id == None:
        return {"msgtype": "logout",
                'state': 1}

    print('before get_msg_box')
    # reflash message box
    status, msg_cache_tuple = get_message_box(self.user_id)
    print('msg_cache_tuple:',msg_cache_tuple)
    if status != 1:
        return {'msgtype': 'msg_list',
                'state': 0}
    print('before del_msg_box')
    delete_message_box(self.user_id)
    msg_id_list = []
    for msg_cache in msg_cache_tuple:
        msg_id_list.append(msg_cache[0])
    status, msg_cache_nickname_list = get_nickname(msg_id_list)
    if status != 1:
        return {'msgtype': 'msg_list',
                'state': 0}

    # print('before get_fri_req')
    #reflash friend request
    status, req_time_id_list = get_friend_request(self.user_id)
    # print('req_time_id_list:', req_time_id_list)
    if status != 1:
        return {'msgtype': 'error',
                'type': 'server:get_friend_request error in msg_reflash'}
    # print('before nick_name:')
    req_id_list = []
    for req_time_id in req_time_id_list:
        req_id_list.append(req_time_id[2])
    status, req_info_list = get_nickname(req_id_list)
    # print('after nickname')
    if status != 1:
        return {'msgtype': 'msg_list',
                'state': 0}

    response = {'msgtype':'msg_list',
                'state':1,
                'list':[]}
    print('req_info_list:',req_info_list)
    for msg_cache in msg_cache_tuple:
        print('msg cache:',msg_cache)
        tmp_dict = {'user1_id':msg_cache[0],
                    'user1_name':msg_cache_nickname_list[msg_cache[0]],
                    'send_date':msg_cache[1] + ' '+ msg_cache[2],
                    'message_type':0,
                    'message':msg_cache[3]}
        print('in msg cache and tmp = ',tmp_dict)
        response['list'].append(tmp_dict)


    for req_time_id in req_time_id_list:
        tmp_dict = {'user1_id':req_time_id[2],
                    'send_date':req_time_id[0] + ' ' + req_time_id[1],
                    'message_type':2,
                    'user1_name':req_info_list[req_time_id[2]][1]}
        response['list'].append(tmp_dict)
    # print('response:',response)
    self.write_message(json.dumps(response))

    # load


def msg_list_rec(self, request_dict):
    # this op need that self.user_id is not None
    if self.user_id == None:
        return {"msgtype": "logout",
                'state': 1}
    delete_message_box(self.user_id)
    return {}


def msg_send(self, request_dict):
    # this op need that self.user_id is not None
    if self.user_id == None:
        return {"msgtype": "logout",
                'state': 1}
    def user_online_func(user_id):
        for user in conn_dict:
            if conn_dict[user].user_id == user_id:
                return True
        return False
    print('go into msg send...')
    conn_dict = gm.get_global_var('connection dict')
    for msg_content in request_dict['list']:
        if 'user2_id' in msg_content:
            user_online = user_online_func(msg_content['user2_id'])
        send_to_other = {'msgtype': 'msg_list',
                         'state':1,
                         'list': []}

        if  msg_content['message_type'] == 0:
            if user_online:
                tmp_dict = {'message_type': msg_content['message_type'],
                            'message': msg_content['message'],
                            'user1_id':self.user_id,
                            'user1_name':self.name,
                            'send_date':msg_content['send_date']}
                send_to_other['list'] = [tmp_dict]
                conn_dict[msg_content['user2_id']].write_message(json.dumps(send_to_other))
            else:
                status = write_message_box(self.user_id, msg_content['user2_id'], msg_content['message'])
                print('msg_content',msg_content)
                if status != 1:
                    return {'msgtype': 'msg_send_rec',
                            'index': request_dict['index'],
                            'state':0}

        elif  msg_content['message_type'] == 1:
            status, group_member_id_list = consult_group_member(msg_content['group_id'])
            if status != 1:
                return {'msgtype': 'msg_send_rec',
                        'index': request_dict['index'],
                        'state': 0}
            for group_member_id in group_member_id_list:
                user_online = user_online_func(group_member_id)
                if user_online:
                    tmp_dict = {'message_type': msg_content['message_type'],
                                'message': msg_content['message'],
                                'user1_id':self.user_id,
                                'user1_name': self.name,
                                'group_id':msg_content['group_id'],
                                'send_date':msg_content['send_date']}
                    send_to_other['list'] = [tmp_dict]
                    conn_dict[group_member_id].write_message(json.dumps(send_to_other))
            # else:
            #     status = write_message_box(self.user_id, msg_content['user2_id'], msg_content['message'])
            #     if status != 1:
            #         return {'msgtype': 'msg_send_rec',
            #                 'state': 0}

        elif msg_content['message_type'] == 2:
            print('message type 2 and user_online:', user_online)
            print('msg_content:',msg_content)
            if user_online:
                tmp_dict = {'message_type': msg_content['message_type'],
                            'user1_id': self.user_id,
                            'user1_name':self.name}
                send_to_other['list'] = [tmp_dict]
                conn_dict[msg_content['user2_id']].write_message(json.dumps(send_to_other))
            else:
                # check if the target user_id exist
                status = make_friend_request(self.user_id, msg_content['user2_id'])
                print(msg_content['user2_id'], ':fri_req:')
                if status == 1:
                    pass
                elif status == -1:
                    pass
                    # return {'msgtype': 'msg_send_rec',
                    #         'state': 0}
                else:
                    return {'msgtype': 'msg_send_rec',
                            'index': request_dict['index'],
                            'state': 0}

        elif msg_content['message_type'] == 3:
            #check if the source user_id exist
            status = add_friends(msg_content['user2_id'], [self.user_id])
            if status != 1:
                return {'msgtype': 'msg_send_rec',
                        'index': request_dict['index'],
                        'state': 0}
            # if user_online:
            #     tmp_dict = {'message_type': msg_content['message_type'],
            #                 'user1_id': self.user_id,
            #                 'user1_name': self.name,
            #                 'send_date': time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())}
            #     send_to_other['list'].append(tmp_dict)
            #     connection_list[user].write_message(json.dumps(send_to_other))

        elif msg_content['message_type'] == 4:
            print('go into msgtype4')
            status = delete_friends(self.user_id, [msg_content['user2_id']])
            print('after delete friends')
            if status != 1:
                return {'msgtype': 'msg_send_rec',
                        'index': request_dict['index'],
                        'state': 0}
            if user_online:
                tmp_dict = {'message_type': msg_content['message_type'],
                            'user1_id': self.user_id,
                            'user1_name': self.name,
                            'send_date': time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())}
                send_to_other['list'] = [tmp_dict]
                conn_dict[msg_content['user2_id']].write_message(json.dumps(send_to_other))

        else:
            return {'msgtype': 'msg_send_rec',
                    'index': request_dict['index'],
                    'state': 0}

    return {'msgtype': 'msg_send_rec',
            'state': 1,
            'index':request_dict['index']}


def get_friend_list(self, request_dict):
    # this op need that self.user_id is not None
    if self.user_id == None:
        return {"msgtype": "logout",
                'state': 1}
    print('before get friends')
    status, friends_user_id = get_friends(self.user_id)
    print('friends user id :', friends_user_id)
    if status != 1:
        return {'msgtype': 'friend_list',
                'state': 0}
    print('before friends nickname')
    status, friends_nickname = get_nickname(friends_user_id)
    print('friends nickname:', friends_nickname)
    if status != 1:
        return {'msgtype': 'friend_list',
                'state': 0}

    friends_list = []
    for i in range(len(friends_user_id)):
        member_tuple = friends_nickname[friends_user_id[i]]
        if member_tuple[0] == 1:
            tmp = {'user_id':friends_user_id[i],
                   'user_nickname':member_tuple[1]}
            friends_list.append(tmp)
    print('friend list:', friends_list)
    response = {'msgtype': 'friend_list',
                'state':1,
                'list': friends_list}
    return response


def friend_list_update(request_dict):
    pass


def change_info(self, request_dict):
    # this op need that self.user_id is not None
    if self.user_id == None:
        return {"msgtype": "logout",
                'state': 1}
    print('go into change info')
    if request_dict['object'] == 'user_nickname':
        print('go into change name')
        if change_nickname(self.user_id, request_dict['change_to']) != 1:
            return {'msgtype': 'change_info',
                    'state': 0}
        self.name = request_dict['change_to']
    elif request_dict['object'] == 'user_password':
        print('go into change passwd')
        if change_password(self.user_id, request_dict['change_to']) != 1:
            return {'msgtype': 'change_info',
                    'state': 0}
    else:
        return {'msgtype': 'change_info',
                'state': 0}
    return {'msgtype': 'change_info',
            'state': 1,
            'object':request_dict['object']}


def create_grp(self, request_dict):
    # this op need that self.user_id is not None
    print('create_grp start..')
    if self.user_id == None:
        return {"msgtype": "logout",
                'state': 1}
    print('go into apply group')
    status, grp_id = new_group(self.user_id)
    if status != 1:
        return {'msgtype': 'apply_group_success',
                'state': 0}
    return {'msgtype':'apply_group_success',
            'state':1,
            'group_id':grp_id}


def join_grp(self, request_dict):
    # this op need that self.user_id is not None
    if self.user_id == None:
        return {"msgtype": "logout",
                'state': 1}
    status = join_group(self.user_id, request_dict['group_id'])
    if status == 1:
        return {'msgtype': 'join_group_success',
                'status': 1}
    elif status == -1:
        return {'msgtype': 'join_group_success',
                'status': 0}
    else:
        return {'msgtype': 'join_group_success',
                'status': 2}


def quit_grp(self, request_dict):
    # this op need that self.user_id is not None
    if self.user_id == None:
        return {"msgtype": "logout",
                'state': 1}
    print('before quit group and req_dict:',request_dict)
    status = quit_group(self.user_id, request_dict['group_id'])
    print('after quit group')
    if status == 0:
        return {'msgtype': 'quit_group',
                'status': 0}
    return {'msgtype': 'quit_group',
            'status': 1}


def get_group_list(self, request_dict):
    # this op need that self.user_id is not None
    if self.user_id == None:
        return {"msgtype": "logout",
                'state': 1}
    status, group_id_list = consult_group(self.user_id)
    if status != 1:
        return {'msgtype': 'group_list',
                'status': 0}
    response = {'msgtype': 'group_list',
                'state':1,
                'list':[]}
    for group_id in group_id_list:
        status, group_member_id_list = consult_group_member(group_id)
        if status == 0:
            return {'msgtype': 'group_list',
                    'status': 0}
        elif status == 1:
            status, group_member_list = get_nickname(group_member_id_list)
            if status != 1:
                return {'msgtype': 'group_list',
                        'status': 0}
            group_member_name_list = []
            for member_id in group_member_list:
                member_tuple = group_member_list[member_id]
                if member_tuple[0] == 1:
                    group_member_name_list.append((member_id,
                                                   member_tuple[1]))
            tmp_dict = {'group_id':group_id,
                        'group_members':group_member_name_list}
            response['list'].append(tmp_dict)

    return response


msgtypes = {'binding':LOGIN,
            'register':Register,
            'logout':logout,
            'unregister':unregister,
            'msg_list_rec':msg_list_rec,
            'msg_send':msg_send,
            'get_friend_list':get_friend_list,
            'change_info':change_info,
            'apply_group':create_grp,
            'join_group':join_grp,
            'quit_group':quit_grp,
            'get_group_list':get_group_list}




#coding:utf-8
import json
import os
import global_manager as gm
# MSG_CACHE = {'p2p':{} , 'g2p':{}, 'friend_request':[], 'friend_agree':[], 'friend_delete':[]}

def load_cache(user_id):
    """
        This function is used to load data of the user with  user_id

        Paremeters
        ----------
        user_id: string

        Return
        ------
        None
    """
    BASE_PATH = os.getcwd()
    filename = os.path.join(BASE_PATH, user_id)
    try:
        with open(filename, 'r') as f:
            local_msg_cache_list = json.loads(f.read())
    except:
        local_msg_cache_list = {'p2p':{} , 'g2p':{}, 'friend_request':[], 'friend_agree':[], 'friend_delete':[]}

    MSG_CACHE = gm.get_global_var('msg_list cache')
    if MSG_CACHE == None:
        gm.set_global_var('msg_list cache', local_msg_cache_list)
    else:
        for message_type in MSG_CACHE:
            if message_type == 'p2p' or message_type == 'g2p':
                for item in local_msg_cache_list[message_type]:
                    if item in MSG_CACHE[message_type]:
                        MSG_CACHE[message_type][item] += local_msg_cache_list[message_type][item]
                    else:
                        MSG_CACHE[message_type][item] = local_msg_cache_list[message_type][item]
            else:
                MSG_CACHE[message_type] += local_msg_cache_list[message_type]


def save_cache(user_id):
    """
        This function is used to save cache of the user with  user_id

        Paremeters
        ----------
        user_id: string
        MSG_CACHE: dict with keys:"p2p", "g2p", "friend_request", "friend_agree", "friend_delete".
        (get more detail about MSG_CACHE by document)

        Return
        ------
        None
    """
    MSG_CACHE = gm.get_global_var('msg_list cache')
    BASE_PATH = os.getcwd()
    filename = os.path.join(BASE_PATH, user_id)
    with open(filename, 'w') as f:
        f.write(json.dumps(MSG_CACHE))
    gm.del_global_var('msg_list cache')


def add_into_cache(msg_list):
    """
        This function is used to add unread message to cache

        Paremeters
        ----------
        msg_list: list of dict with keys: "user1_id", "user1_name", "message_type" definitely
        MSG_CACHE: dict with keys:"p2p", "g2p", "friend_request", "friend_agree", "friend_delete".
        (get more detail about MSG_CACHE by document)

        Return
        ------
        status
        status:
            0: dict error
            1: success
    """
    MSG_CACHE = gm.get_global_var('msg_list cache')
    if MSG_CACHE == None:
        MSG_CACHE = {'p2p': {}, 'g2p': {}, 'friend_request': [], 'friend_agree': [], 'friend_delete': []}
        gm.set_global_var('msg_list cache', MSG_CACHE)

    for msg in msg_list:

        if msg['message_type'] == 0:
            tmp_dict = {'user_name': msg['user1_name'],
                        'send_date': msg['send_date'],
                        'message': msg['message']}
            if msg['user1_id'] in MSG_CACHE['p2p']:
                MSG_CACHE['p2p'][msg['user1_id']].append(tmp_dict)
            else:
                MSG_CACHE['p2p'][msg['user1_id']] = [tmp_dict]

        elif msg['message_type'] == 1:
            tmp_dict = {'user_id':msg['user1_id'],
                        'user_name': msg['user1_name'],
                        'send_date': msg['send_date'],
                        'message': msg['message']}
            if msg['group_id'] in MSG_CACHE['g2p']:
                MSG_CACHE['g2p'][msg['group_id']].append(tmp_dict)
            else:
                MSG_CACHE['g2p'][msg['group_id']] = [tmp_dict]

        elif msg['message_type'] == 2:
            tmp_dict = {'user_name': msg['user1_name'],
                        'user_id':msg['user1_id']}
            MSG_CACHE['friend_request'].append(tmp_dict)

        elif msg['message_type'] == 3:
            tmp_dict = {'user_name': msg['user1_name'],
                        'user_id': msg['user1_id']}
            MSG_CACHE['friend_agree'].append(tmp_dict)

        elif msg['message_type'] == 4:
            tmp_dict = {'user_name': msg['user1_name'],
                        'user_id': msg['user1_id']}
            MSG_CACHE['friend_delete'].append(tmp_dict)

        else:
            return 0
    return 1


def get_from_cache(op_dict):
    """
        This function is used to get unread message

        Paremeters
        ----------
        op_dict: dict (all keys below are optional)
            "user_ids": list
            "group_ids": list
            "friend_request": int
            "friend_agree": int
            "friend_delete": int
            (about "friend_request", "friend_agree", "friend_delete":
            if you want to get limit pieces of message, input positive number;
            if you want to get all message, input 0)

        Return
        ------
        dict:
            just like global variable MSG_CACHE
    """
    MSG_CACHE = gm.get_global_var('msg_list cache')
    cache = {}
    #print('in get_from_cache begin MSG_CACHE:',MSG_CACHE)
    if 'user_ids' in op_dict:
        cache['p2p'] = {}
        for user_id in op_dict['user_ids']:
            if user_id in MSG_CACHE['p2p']:
                cache['p2p'][user_id] = MSG_CACHE['p2p'][user_id]
                del MSG_CACHE['p2p'][user_id]
        if op_dict['user_ids'][0] in cache['p2p']:
            return cache['p2p'][op_dict['user_ids'][0]]
        else:
            return []

    if 'group_ids' in op_dict:
        cache['g2p'] = {}
        for group_id in op_dict['group_ids']:
            if group_id in MSG_CACHE['g2p']:
                cache['g2p'][group_id] = MSG_CACHE['g2p'][group_id]
                del MSG_CACHE['g2p'][group_id]
        if op_dict['group_ids'][0] in cache['g2p']:
            return cache['g2p'][op_dict['group_ids'][0]]
        else:
            return []

    if 'friend_request' in op_dict:
        if op_dict['friend_request'] > 0:
            cache['friend_request'] = MSG_CACHE['friend_request'][0:op_dict['friend_request']]
            MSG_CACHE['friend_request'] = MSG_CACHE['friend_request'][op_dict['friend_request']:]
        elif op_dict['friend_request'] == 0:
            cache['friend_request'] = MSG_CACHE['friend_request']
            MSG_CACHE['friend_request'] = []
        else:
            cache['friend_request'] = []
        return cache['friend_request']

    if 'friend_agree' in op_dict:
        if op_dict['friend_agree'] > 0:
            cache['friend_agree'] = MSG_CACHE['friend_agree'][0:op_dict['friend_agree']]
            MSG_CACHE['friend_agree'] = MSG_CACHE['friend_agree'][op_dict['friend_agree']:]
        elif op_dict['friend_agree'] == 0:
            cache['friend_agree'] = MSG_CACHE['friend_agree']
            MSG_CACHE['friend_agree'] = []
        else:
            cache['friend_agree'] = []
        return cache['friend_agree']

    if 'friend_delete' in op_dict:
        if op_dict['friend_delete'] > 0:
            cache['friend_delete'] = MSG_CACHE['friend_delete'][0:op_dict['friend_delete']]
            MSG_CACHE['friend_delete'] = MSG_CACHE['friend_delete'][op_dict['friend_delete']:]
        elif op_dict['friend_delete'] == 0:
            cache['friend_delete'] = MSG_CACHE['friend_delete']
            MSG_CACHE['friend_delete'] = []
        else:
            cache['friend_delete'] = []
        return cache['friend_delete']
    #print('in get_from_cache the cache:',cache)
    #return cache
    return []

# print('cache:',MSG_CACHE)
# add_into_cache([{'user1_id': '0000000000000', 'send_date': '2020-06-20 17:49:42', 'message_type': 2, 'user1_name': 'zero'}])
# print('cache:',MSG_CACHE)
# print('get cache:', get_from_cache({'friend_request':0}))
# print('cache:',MSG_CACHE)
# save_cache('0000000000001')
import sys

sys.path.append('..')

import time

import global_manager as gm
import db.db_tools as tools
import db.id_string_processing as idstr_proc


def register_user(user_info):
    """
    This function is used to register a user
    Parameters
    ----------
    user_info: dictionary
        keys: nickname, password
    Return
    ------
    (status, None/id)
    status:
    0: database connection error
    1: success
    when success, return id, else return None
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0, None
    # get now time and password
    time_stamp = int(time.time())
    local_time = time.localtime(time_stamp)
    register_date = '%.4d-%.2d-%.2d' % (local_time[0], local_time[1], local_time[2])
    register_time = '%.2d:%.2d:%.2d' % (local_time[3], local_time[4], local_time[5])
    encrypted_password = idstr_proc.encrypte_password(user_info['password'], str(time_stamp))
    # get user_id
    pool_file = open(gm.get_global_var('user id pool path'), 'rt')
    pool = pool_file.readlines()
    pool_file.close()
    pool_ids = pool[0].replace('\n', '')
    if len(pool_ids):
        pool_flag = 1
        pool_ids = pool_ids.split(',')
        register_id = pool_ids.pop()
    else:
        pool_flag = 0
        cnt_file = open(gm.get_global_var('user id cnt path'), 'rt')
        cnt = cnt_file.readlines()
        cnt_file.close()
        register_id = cnt[0].replace('\n', '')
    # write to database
    sql_order = "insert into user_information (user_id,user_nickname,update_pwd_date,update_pwd_time,user_password) \
                  values ('%s','%s','%s','%s','%s')" % (register_id, user_info['nickname'], register_date, register_time, encrypted_password)
    try:
        affect_row = cursor.execute(sql_order)
        if not affect_row:
            raise Exception
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
        tools.close_database(cursor, connection)
        return 0, None
    tools.close_database(cursor, connection)
    # write into pool or cnt file
    if pool_flag:
        pool[0] = '%s\n' % ','.join(pool_ids)
        pool_file = open(gm.get_global_var('user id pool path'), 'wt')
        pool_file.writelines(pool)
        pool_file.close()
    else:
        cnt[0] = '%s\n' % idstr_proc.string_plus_plus(register_id)
        cnt_file = open(gm.get_global_var('user id cnt path'), 'wt')
        cnt_file.writelines(cnt)
        cnt_file.close()
    return 1, register_id


def login(user_id, password):
    """
    This function is used to confirm the identity of the user
    Parameters
    ----------
    user_id: string
        The user to login
    password: string
        The password the user offered
    Reuturn
    -------
    -2: user not exist
    -1: password incorrect
    0: database connection error
    1: success, ok
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0
    # get the password
    sql_order = "select update_pwd_date,update_pwd_time,user_password from user_information where user_id='%s'" % user_id
    cursor.execute(sql_order)
    consult_result = cursor.fetchall()
    tools.close_database(cursor, connection)
    # check password
    if len(consult_result):
        consult_result = consult_result[0]
        correct_password = consult_result[2]
        pwd_date = consult_result[0]
        pwd_date = pwd_date.strftime('%Y-%m-%d')
        pwd_time = consult_result[1]
        pwd_time = '%d:%d:%d' % (pwd_time.seconds // 3600, pwd_time.seconds // 60 -
                                 60 * (pwd_time.seconds // 3600), pwd_time.seconds % 60)
        pwd_updated_moment = '%s %s' % (pwd_date, pwd_time)
        time_array = time.strptime(pwd_updated_moment, '%Y-%m-%d %H:%M:%S')
        pwd_updated_time = int(time.mktime(time_array))
        input_password = idstr_proc.encrypte_password(password, str(pwd_updated_time))
        if input_password == correct_password:
            return 1
        else:
            return -1
    else:
        return -2


def get_nickname(user_ids):
    """
    This function is used to consult the nickname of users
    user_ids: list/tuple/set of string
        The users to consult nickname
    Return
    ------
    (status, None/dictionary of nicknames)
        The values are (0/1, nickname) 0: user does not exist, 1: user exists
    status:
    0: database connection error
    1: success
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0
    # consult result
    nicknames = dict()
    for each in user_ids:
        sql_order = "select user_nickname from user_information where user_id='%s'" % each
        cursor.execute(sql_order)
        consult_result = cursor.fetchall()
        if len(consult_result):
            nicknames[each] = (1, consult_result[0][0])
        else:
            nicknames[each] = (0, '')
    tools.close_database(cursor, connection)
    return 1, nicknames


def change_nickname(user_id, new_nickname):
    """
    This function is used to change the nickname of a user
    Paremeters
    ----------
    user_id: string
        The user to change nickname
    new_nickname: string
        New nickname
    Return
    ------
    0: database connection error
    1: success
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0
    # write into database
    sql_order = "update user_information set user_nickname='%s' where user_id='%s'" % (new_nickname, user_id)
    try:
        affect_row = cursor.execute(sql_order)
        if not affect_row:
            raise Exception
        connection.commit()
    except:
        connection.rollback()
        tools.close_database(cursor, connection)
        return 0
    tools.close_database(cursor, connection)
    return 1


def change_password(user_id, new_password):
    """
    This function is used to change the password of a user
    Parameters
    ----------
    user_id: string
        The user to change password
    new_password: string
        New password
    Return:
    0: database connection error
    1: success
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0
    # calculate the time now and encrypte password
    time_stamp = int(time.time())
    local_time = time.localtime(time_stamp)
    now_date = '%.4d-%.2d-%.2d' % (local_time[0], local_time[1], local_time[2])
    now_time = '%.2d:%.2d:%.2d' % (local_time[3], local_time[4], local_time[5])
    encrypted_password = idstr_proc.encrypte_password(new_password, str(time_stamp))
    # write into database
    sql_order = "update user_information set update_pwd_date='%s',update_pwd_time='%s',user_password='%s' where user_id='%s'" % (
        now_date, now_time, encrypted_password, user_id)
    try:
        affect_row = cursor.execute(sql_order)
        if not affect_row:
            raise Exception
        connection.commit()
    except:
        connection.rollback()
        tools.close_database(cursor, connection)
        return 0
    tools.close_database(cursor, connection)
    return 1


def add_friends(source_user, target_users):
    """
    This function is used to add a friend
    source_user: string
        source user id
    target_users: list/tuple/set of string
        target user id
    Return
    ------
    0: database connection error
    1: success
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
    # reform data
    sql_data = []
    for each_id in target_users:
        sql_data.append((source_user, each_id))
        sql_data.append((each_id, source_user))
    # write into database
    sql_order = "insert into user_friends (user1_id, user2_id) values (%s,%s)"
    try:
        affect_row = cursor.executemany(sql_order, sql_data)
        if affect_row != len(sql_data):
            raise Exception
        connection.commit()
    except:
        connection.rollback()
        tools.close_database(cursor, connection)
        return 0
    tools.close_database(cursor, connection)
    return 1


def get_friends(source_user):
    """
    This function is used to consult friends of a user
    source_user: string
        The id of the user
    Return
    ------
    (status, None/list of friend user ids)
    status:
    0: database connection error
    1L success
    """
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0, None
    # get friends
    sql_order = "select user2_id from user_friends where user1_id ='%s'" % source_user
    cursor.execute(sql_order)
    consult_result = cursor.fetchall()
    tools.close_database(cursor, connection)
    # reform result
    friends = []
    for each in consult_result:
        friends.append(each[0])
    return 1, friends


def delete_friends(source_id, target_ids):
    """
    This function is used to delete friends
    Parameters
    ----------
    source_id: string
        The source user to delete friend
    target_ids: list/tuple/set of string
        The users to delete friend
    Return
    ------
    0: database connection error
    1: success
    """
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0
    # structure sql order
    sql_data = []
    for each in target_ids:
        sql_data.append((source_id, each))
        sql_data.append((each, source_id))
    sql_order = "delete from user_friends where user1_id=%s and user2_id=%s"
    # write into database
    try:
        cursor.executemany(sql_order, sql_data)
        connection.commit()
    except:
        connection.rollback()
        tools.close_database(cursor, connection)
        return 0
    tools.close_database(cursor, connection)
    return 1


def new_group(user_id):
    """
    This function is used to form a new group chat number
    user_id: String
        The people who calls for the group
    Return
    ------
    (status, None/group_id)
    status:
    0: database connection error
    1: success
    if success, will return the group id, else return None
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0, None
    # get a new group id
    pool_file = open(gm.get_global_var('group id pool path'), 'rt')
    pool = pool_file.readlines()
    pool_file.close()
    pool_ids = pool[0].replace('\n', '')
    if len(pool_ids):
        pool_flag = 1
        pool_ids = pool_ids.split(',')
        group_id = pool_ids.pop()
    else:
        pool_flag = 0
        cnt_file = open(gm.get_global_var('group id cnt path'), 'rt')
        cnt = cnt_file.readlines()
        cnt_file.close()
        group_id = cnt[0].replace('\n', '')
    # write into databse
    sql_order = "insert into user_group (user_id,group_id) values ('%s','%s')" % (user_id, group_id)
    try:
        affect_row = cursor.execute(sql_order)
        if not affect_row:
            raise Exception
        connection.commit()
    except:
        connection.rollback()
        tools.close_database(cursor, connection)
        return 0, None
    tools.close_database(cursor, connection)
    # write into pool or cnt file
    if pool_flag:
        pool[0] = '%s\n' % ','.join(pool_ids)
        pool_file = open(gm.get_global_var('group id pool path'), 'wt')
        pool_file.writelines(pool)
        pool_file.close()
    else:
        cnt[0] = '%s\n' % idstr_proc.string_plus_plus(group_id)
        cnt_file = open(gm.get_global_var('group id cnt path'), 'wt')
        cnt_file.writelines(cnt)
        cnt_file.close()
    return 1, group_id


def join_group(user_id, group_id):
    """
    This function is used to join an existing group
    user_id: string
        The user to join the group
    group_id: string
        The id of the target group
    Return
    ------
    -1: group not exist
    0: database connection error
    1: success
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0
    # consult the existence of the group
    sql_order = "select * from user_group where group_id='%s'" % group_id
    cursor.execute(sql_order)
    if not len(cursor.fetchall()):
        tools.close_database(cursor, connection)
        return -1
    # consult whether joint, if joint don't join again
    sql_order = "select * from user_group where group_id='%s' and user_id='%s'" % (group_id, user_id)
    cursor.execute(sql_order)
    if len(cursor.fetchall()):
        tools.close_database(cursor, connection)
        return 1
    # join the group
    sql_order = "insert into user_group (user_id,group_id) values ('%s','%s')" % (user_id, group_id)
    try:
        affect_row = cursor.execute(sql_order)
        if not affect_row:
            raise Exception
        connection.commit()
    except:
        connection.rollback()
        tools.close_database(cursor, connection)
        return 0
    tools.close_database(cursor, connection)
    return 1


def quit_group(user_id, group_id):
    """
    This function is used to quit a group chat
    Parametes
    ---------
    user_id: string
        The user to quit the group
    group_id: string
        The group_id of the group to quit
    Return
    ------
    -1: did not join the group
    0: database connection error
    1: success
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0
    # delete from the databse
    sql_order = "delete from user_group where user_id='%s' and group_id='%s'" % (user_id, group_id)
    try:
        affect_row = cursor.execute(sql_order)
    except:
        connection.rollback()
        tools.close_database(cursor, connection)
        return 0
    # consult whether this group has number
    sql_order = "select * from user_group where group_id='%s'" % group_id
    cursor.execute(sql_order)
    if not len(cursor.fetchall()):  # this is an empty group, restore it into the pool
        pool_file = open(gm.get_global_var('group id pool path'), 'rt')
        pool = pool_file.readlines()
        pool_file.close()
        pool_ids = pool[0].replace('\n', '')
        if len(pool_ids):
            pool[0] = pool_ids + ',%s\n' % group_id
        else:
            pool[0] = '%s\n' % group_id
        pool_file = open(gm.get_global_var('group id pool path'), 'wt')
        pool_file.writelines(pool)
        pool_file.close()
    connection.commit()
    tools.close_database(cursor, connection)
    if affect_row:
        return 1
    else:
        return -1


def consult_group_member(group_id):
    """
    This function is used to consult the group members of a group
    Parameters
    ----------
    group_id: string
        The group id to consult
    Return
    ------
    (status, None/list of group member user_id)
    status:
    -1: group not exist
    0: database connection error
    1: success
    if success, will return the list, else return None
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0, None
    # consult result
    sql_order = "select user_id from user_group where group_id='%s'" % group_id
    cursor.execute(sql_order)
    consult_result = cursor.fetchall()
    tools.close_database(cursor, connection)
    # reform the result
    if len(consult_result):
        group_list = []
        for each in consult_result:
            group_list.append(each[0])
        return 1, group_list
    else:
        return -1, None


def consult_group(user_id):
    """
    This function is used to consult the group ids of a user
    user_id: string
        The user to consult
    Return
    ------
    (status, None/list of group_ids)
    status:
    0: database connection error
    1: success
    if success, will return the list
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0, None
    # consult results
    sql_order = "select group_id from user_group where user_id='%s'" % user_id
    cursor.execute(sql_order)
    consult_result = cursor.fetchall()
    tools.close_database(cursor, connection)
    group_ids = []
    for each in consult_result:
        group_ids.append(each[0])
    return 1, group_ids

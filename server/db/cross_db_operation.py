import sys
import time

sys.path.append('..')

import global_manager as gm
import db.db_tools as tools


def unregister_user(user_id):
    """
    This function is used to unregister a user
    Parameters
    ----------
    user_id: string
        The user to unregister
    Return
    ------
    0: database connection error
    1: success
    """
    # connect database
    try:
        connection_user, cursor_user = tools.open_database('linux_meeting_users')
        connection_msgbox, cursor_msgbox = tools.open_database('linux_meeting_message_box')
    except:
        try:
            tools.close_database(cursor_user, connection_user)
            tools.close_database(cursor_msgbox, connection_msgbox)
        except:
            pass
        return 0
    # delete from message box
    sql_order = "delete from message_box where source_user_id='%s' or target_user_id='%s'" % (user_id, user_id)
    try:
        cursor_msgbox.execute(sql_order)
    except:
        connection_msgbox.rollback()
        tools.close_database(cursor_user, connection_user)
        tools.close_database(cursor_msgbox, connection_msgbox)
        return 0
    # delete from user_information
    sql_order = "select group_id from user_group where user_id='%s'" % user_id
    sql_order1 = "delete from user_friends where user1_id='%s' or user2_id='%s'" % (user_id, user_id)
    sql_order2 = "delete from user_group where user_id='%s'" % user_id
    sql_order3 = "delete from user_information where user_id='%s'" % user_id
    cursor_user.execute(sql_order)
    consult_result = cursor_user.fetchall()
    try:
        cursor_user.execute(sql_order1)
        cursor_user.execute(sql_order2)
        cursor_user.execute(sql_order3)
    except:
        connection_user.rollback()
        connection_msgbox.rollback()
        connection_msgbox.rollback()
        tools.close_database(cursor_user, connection_user)
        tools.close_database(cursor_msgbox, connection_msgbox)
        return 0
    connection_user.commit()
    connection_msgbox.commit()
    # write to pool file
    # group id
    group_ids = []
    for each in consult_result:
        sql_order = "select * from user_group where group_id='%s'" % each[0]
        cursor_user.execute(sql_order)
        if not len(cursor_user.fetchall()):
            group_ids.append(each[0])
    tools.close_database(cursor_user, connection_user)
    tools.close_database(cursor_msgbox, connection_msgbox)
    if len(group_ids):
        pool_file = open(gm.get_global_var('group id pool path'), 'rt')
        pool = pool_file.readlines()
        pool_file.close()
        pool_ids = pool[0].replace('\n', '')
        if len(pool_ids):
            pool[0] = pool_ids + ',' + ','.join(group_ids) + '\n'
        else:
            pool[0] = '%s\n' % ','.join(group_ids)
        pool_file = open(gm.get_global_var('group id pool path'), 'wt')
        pool_file.writelines(pool)
        pool_file.close()
        # user id
    pool_file = open(gm.get_global_var('user id pool path'), 'rt')
    pool = pool_file.readlines()
    pool_file.close()
    pool_ids = pool[0].replace('\n', '')
    if len(pool_ids):
        pool[0] = pool_ids + ',%s\n' % user_id
    else:
        pool[0] = '%s\n' % user_id
    pool_file = open(gm.get_global_var('user id pool path'), 'wt')
    pool_file.writelines(pool)
    pool_file.close()
    return 1


def make_friend_request(source_user_id, target_user_id):
    """
    This function is used to send a friend request
    Parameters
    ----------
    source_user_id: string
        The source user send this friend request
    target_user_id: string
        The target user
    Return
    ----------
    -1: target user does not exist
    0: database connection error
    1: success
    """
    # connect user database
    try:
        connection, cursor = tools.open_database('linux_meeting_users')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0
    sql_order = "select * from user_information where user_id='%s'" % target_user_id
    cursor.execute(sql_order)
    if not len(cursor.fetchall()):
        tools.close_database(cursor, connection)
        return -1
    tools.close_database(cursor, connection)
    # connect message box database
    try:
        connection, cursor = tools.open_database('linux_meeting_message_box')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0
    # calculate time
    time_stamp = int(time.time())
    local_time = time.localtime(time_stamp)
    send_date = '%.4d-%.2d-%.2d' % (local_time[0], local_time[1], local_time[2])
    send_time = '%.2d:%.2d:%.2d' % (local_time[3], local_time[4], local_time[5])
    # write into database
    sql_order = "insert into message_box (source_user_id,target_user_id,send_date,send_time,message_type,message) \
                   values ('%s','%s','%s','%s',%d,'%s')" % (source_user_id, target_user_id, send_date, send_time, 1, '')
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
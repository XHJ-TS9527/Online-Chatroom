import time

import db.db_tools as tools


def get_friend_request(user_id):
    """
    This function is used to get the friend request
    Parameters
    ----------
    user_id: string
        The target user
    Return
    ------
    (status,None/List of source user_id)
    status:
    0: database connection error
    1: success
    if success, will return tuple of tuples (send date, send time, source user id)
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_message_box')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0, None
    # get all the request
    sql_order = "select send_date,send_time,source_user_id from message_box where target_user_id='%s' and message_type=1" % user_id
    cursor.execute(sql_order)
    consult_result = cursor.fetchall()
    print(consult_result)
    # reform result
    quest_info = []
    for each in consult_result:
        quest_date = each[0].strftime('%Y-%m-%d')
        quest_time = each[1]
        quest_time = '%d:%d:%d' % (quest_time.seconds // 3600, quest_time.seconds // 60
                                   - 60 * (quest_time.seconds // 3600), quest_time.seconds % 60)
        quest_info.append((quest_date, quest_time, each[2]))
    # delete these records
    sql_order = "delete from message_box where target_user_id='%s' and message_type=1" % user_id
    try:
        cursor.execute(sql_order)
        connection.commit()
    except:
        connection.rollback()
        tools.close_database(cursor, connection)
        return 0
    tools.close_database(cursor, connection)
    return 1, quest_info


def write_message_box(source_user_id, target_user_id, message):
    """
    This function is used to write unreceived message in the message box
    Parameters
    ----------
    source_user_id: string
        The user_id of sender
    target_user_id: string
        The user_id of receiver
    message: string
        The message to store
    Return
    ------
    0: database connection error
    1: success
    """
    # connect database
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
    operation_date = '%.4d-%.2d-%.2d' % (local_time[0], local_time[1], local_time[2])
    operation_time = '%.2d:%.2d:%.2d' % (local_time[3], local_time[4], local_time[5])
    # write into database
    sql_order = "insert into message_box (source_user_id,target_user_id,send_date,send_time,message_type,message) values \
            ('%s','%s','%s','%s',%d,'%s')" % (source_user_id, target_user_id, operation_date, operation_time,
                0, message)
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


def get_message_box(consult_user_id):
    """
    This function is used to get the unread message stored in the message box
    Parameters
    ----------
    consult_user_id: string
        The receiver user_id
    Return
    ------
    (status,None/tuple of (sender_id,send_date,send_time,message))
    status:
    0: database connection error
    1: success
    if success, will return tuple of (sender_id,send_date,send_time,message)
    """
    # connect database
    try:
        connection, cursor = tools.open_database('linux_meeting_message_box')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0, None
    # get results
    sql_order = "select source_user_id,send_date,send_time,message from message_box where target_user_id='%s' and \
                   message_type=0" % consult_user_id
    cursor.execute(sql_order)
    consult_result = cursor.fetchall()
    # reform result
    message_info = []
    for each in consult_result:
        quest_date = each[1].strftime('%Y-%m-%d')
        quest_time = each[2]
        quest_time = '%d:%d:%d' % (quest_time.seconds // 3600, quest_time.seconds // 60
                                   - 60 * (quest_time.seconds // 3600), quest_time.seconds % 60)
        message_info.append((each[0], quest_date, quest_time, each[3]))
    tools.close_database(cursor, connection)
    return 1, message_info


def delete_message_box(consult_user_id):
    """
    This function is used to delete the messages send from messagebox
    Parameters
    ----------
    consult_user_id: string
        The receiver user_id
    Return
    ------
    0: database connection error
    1: success
    """
    try:
        connection, cursor = tools.open_database('linux_meeting_message_box')
    except:
        try:
            tools.close_database(cursor, connection)
        except:
            pass
        return 0
    # delete these data
    sql_order = "delete from message_box where target_user_id='%s' and message_type=0" % consult_user_id
    try:
        cursor.execute(sql_order)
        connection.commit()
    except:
        connection.rollback()
        tools.close_database(cursor, connection)
        return 0
    tools.close_database(cursor, connection)
    return 1

# import moudules
import sys
import time

sys.path.append('..')
sys.path.append('.')
import pymysql

import global_manager as gm


def db_path_init():
    # some variables
    db_host = 'localhost'
    db_port = 3306
    db_user = 'root'
    db_pwd = '123456'
    user_id_cnt_txt_path = '/home/linux_meeting/db/pool_CNT/user_id_counter.txt'
    user_id_pool_txt_path = '/home/linux_meeting/db/pool_CNT/user_id_pool.txt'
    group_id_cnt_txt_path = '/home/linux_meeting/db/pool_CNT/group_id_counter.txt'
    group_pool_txt_path = '/home/linux_meeting/db/pool_CNT/group_id_pool.txt'
    # set dictionary
    gm.set_global_var('mysql host', db_host)
    gm.set_global_var('mysql port', db_port)
    gm.set_global_var('mysql user', db_user)
    gm.set_global_var('mysql password', db_pwd)
    gm.set_global_var('user id cnt path', user_id_cnt_txt_path)
    gm.set_global_var('user id pool path', user_id_pool_txt_path)
    gm.set_global_var('group id cnt path', group_id_cnt_txt_path)
    gm.set_global_var('group id pool path', group_pool_txt_path)


def open_database(database_name):
    config = {'host': gm.get_global_var('mysql host'), 'port': gm.get_global_var('mysql port'),
              'user': gm.get_global_var('mysql user'), 'password': gm.get_global_var('mysql password'),
              'db': database_name, 'charset': 'utf8'}
    connection = pymysql.connect(**config)
    return connection, connection.cursor()


def close_database(cursor, connection):
    cursor.close()
    connection.close()


def reset_db():
    """
    This function is used to reset the database
    """
    # databases
    config = {'host': gm.get_global_var('mysql host'), 'port': gm.get_global_var('mysql port'),
              'user': gm.get_global_var('mysql user'), 'password': gm.get_global_var('mysql password'),
              'db': 'linux_meeting_users', 'charset': 'utf8'}
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    sql_order1 = "truncate user_information"
    sql_order2 = "truncate user_friends"
    sql_order3 = "truncate user_group"
    cursor.execute(sql_order1)
    cursor.execute(sql_order2)
    cursor.execute(sql_order3)
    connection.commit()
    cursor.close()
    connection.close()
    config['db'] = 'linux_meeting_message_box'
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    sql_order = "truncate message_box"
    cursor.execute(sql_order)
    connection.commit()
    cursor.close()
    connection.close()
    # write pool files
    pool_file = open(gm.get_global_var('user id pool path'), 'wt')
    pool_file.writelines(['\n'])
    pool_file.close()
    pool_file = open(gm.get_global_var('group id pool path'), 'wt')
    pool_file.writelines(['\n'])
    pool_file.close()
    # write cnt files
    cnt_file = open(gm.get_global_var('user id cnt path'), 'wt')
    cnt_file.writelines(['0' * 13 + '\n'])
    cnt_file.close()
    cnt_file = open(gm.get_global_var('group id cnt path'), 'wt')
    cnt_file.writelines(['0' * 50 + '\n'])
    cnt_file.close()

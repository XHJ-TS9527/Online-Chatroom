def gm_init():
    global global_var_dict
    global_var_dict = dict()


def set_global_var(var_name, var_value):
    global global_var_dict
    global_var_dict[var_name] = var_value


def get_global_var(var_name):
    global global_var_dict
    return global_var_dict.get(var_name, None)


def del_global_var(var_name):
    global global_var_dict
    del global_var_dict[var_name]


def gm_del():
    global global_var_dict
    del global_var_dict

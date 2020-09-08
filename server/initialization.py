import global_manager as gm
import db.db_tools as tools


def initialization_main():
    gm.gm_init()
    tools.db_path_init()
    #tools.reset_db()

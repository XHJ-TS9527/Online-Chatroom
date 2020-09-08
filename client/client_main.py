import client.global_manager as gm
import client.client_interface as interface


class main():

    def main(self):
        self.init()
        core = interface.client_main()
        support_UI = input("您的系统是否支持图形界面[Y/N]:")
        while support_UI not in ('Y', 'N'):
            print('输入有误,请重新输入.')
            support_UI = input("您的系统是否支持图形界面[Y/N]:")
        if support_UI == 'Y':
            core.have_GUI()
        else:
            core.no_GUI()
        gm.gm_del()
        print('感谢您的使用')

    def init(self):
        gm.gm_init()
        gm.set_global_var('network send cache', [])
        gm.set_global_var('network receive cache', [])
        gm.set_global_var('stop flag', 0)
        gm.set_global_var('connection broken', 1)
        gm.set_global_var('friend request cnt', 0)
        gm.set_global_var('friend add cnt', 0)
        gm.set_global_var('friend delete cnt', 0)
        gm.set_global_var('privacy chat cnt', 0)
        gm.set_global_var('group chat cnt', 0)
        gm.set_global_var('try times', 3)


if __name__ == '__main__':
    M = main()
    M.main()
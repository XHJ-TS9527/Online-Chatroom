server为服务器程序，其中db文件夹内为数据库程序。server程序本地不可运行，因为MySQL数据库是设置在我们（真实网络）的服务器上的。
client分为三个文件夹，请根据版本选择运行。运行的程序是client_main.py，其余程序为支撑程序，用户交互层为interface，业务接口层为core，网络层为network_service。
GUI界面目前开发完成，需要Python安装了tkinter库才可以实现。
服务器调整已经完成，老师可以运行程序使用。

注意，图形界面支持要求Python已经安装tkinter包，否则会报错。
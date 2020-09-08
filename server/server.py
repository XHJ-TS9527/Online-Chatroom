
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop


import argparse
import json

from data_processing import *
import initialization
import global_manager as gm


class ReqHandler(WebSocketHandler):

    def open(self, *args, **kwargs):
        init_base_func(self)
        # print('add type:',type(self.request.connection.context.address))
        print(self.request.connection.context.address, 'connect!')
        response_success = {"msgtype":"connect_succeed"}
        self.write_message(json.dumps(response_success))

    def on_message(self, message):
        request_dict = json.loads(message)
        try:
            if request_dict.get('msgtype') == 'heart':
                response_dict = {'msgtype': 'heart'}
            else:
                print('before data procesing', '-'*50)
                print('操作前,当前在线人数:', len(gm.get_global_var('connection dict')))
                print('user_id:', self.user_id)
                print('the msgtype is ', request_dict['msgtype'])
                response_dict = msgtypes[request_dict['msgtype']](self, request_dict)
                print('response_dict', response_dict)
                print('user_id:', self.user_id)
                print('操作后,当前在线人数:', len(gm.get_global_var('connection dict')))
                print('after data processing', '-'*50)
        except:
            print([self.request.connection.context.address] + [self.user_id], ' : client disconnect!')
            init_base_func(self)
            response_dict = {'msgtype': 'error',
                            'type':'fallout'}
        if response_dict != {}:
            response = json.dumps(response_dict)
            self.write_message(response)
            # if (request_dict['msgtype'] == 'binding') and (response_dict['state'] == 0):
            #     import time
            #     time.sleep(1.5)
            #     msg_reflash(self)

    def on_close(self):
        conn_dict = gm.get_global_var('connection dict')
        for user_id in conn_dict:
            if conn_dict[user_id] == self:
                del conn_dict[user_id]
                break
        print([self.request.connection.context.address] + [self.user_id], ' : host disconnect!')

    def check_origin(self, origin):
        return True

def main(args):
    gm.set_global_var('connection dict', {})
    port = args.port
    app = Application([
        (r'^/$', ReqHandler),
    ])
    http_server = HTTPServer(app, xheaders=True)
    http_server.listen(port)
    IOLoop.instance().start()


if __name__ == "__main__":
    initialization.initialization_main()
    parser = argparse.ArgumentParser(description="help info")
    parser.add_argument("-p", "--port", default=8020, help="the port number", type=int, dest="port")
    args = parser.parse_args()
    main(args)


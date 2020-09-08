import asyncio
import json

import global_manager as gm
import client.cache_opreration as cache

import websockets

class network_tool():

    def __init__(self):
        self.target = ''wss://scut-bookpot.top:8010/linux_meeting'

    async def start_network_core(self):
        self.socket = await websockets.connect(self.target)
        task = [self.always_send_msg(), self.always_receive_msg()]
        await asyncio.gather(*task)
    
    def start_network(self):
        asyncio.run(self.start_network_core())

    async def always_send_msg(self):
        while 1:
            try:
                await asyncio.sleep(0.1)
                if not gm.get_global_var('connection broken'):
                    while len(gm.get_global_var('network send cache')):
                        last_section = gm.get_global_var('network send cache')[0]
                        await self.socket.send(last_section)
                        gm.remove_global_var_list_item('network send cache', last_section)
                    if gm.get_global_var('stop flag'):
                        break
            except Exception as e:
                if not gm.get_global_var('connection broken'):
                    print('网络发送发生异常')
                    print(e)
                    gm.set_global_var('connection broken', 1)
                    break

    async def always_receive_msg(self):
        while 1:
            try:
                await asyncio.sleep(0.1)
                response_json = await self.socket.recv()
                receive_info = json.loads(response_json)
                if receive_info['msgtype'] == 'msg_list':
                    cache.add_into_cache(receive_info['list'])
                else:
                    gm.append_global_var_list_item('network receive cache', receive_info)
                if gm.get_global_var('stop flag'):
                    break
            except Exception as e:
                if not gm.get_global_var('connection broken'):
                    print('网络接收发生异常')
                    print(e)
                    gm.set_global_var('connection broken', 1)
                    break

    async def disconnect_server_core(self):
        await self.socket.close(reason='User exit')
    
    def disconect_server(self):
        asyncio.run(disconnect_server_core())

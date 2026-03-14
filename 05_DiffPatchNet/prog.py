#!/usr/bin/env python3
import asyncio
import cowsay
import shlex

clients = {}

class Client:
    def __init__(self):
        self.name = None
        self.queue = asyncio.Queue() 

async def chat(reader, writer):
    flag_quit = False
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = Client()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].queue.get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                arg = shlex.split(q.result().decode())
                
                if (arg[0] == "login") and len(arg) == 2:
                    # login название_коровы — зарегистрироваться под именем название_коровы
                    name_cow = arg[1]
                    if name_cow in clients:
                        writer.write(f"Error. This name is already taken.\n".encode())
                        break
                    clients[me].name = name_cow
                    writer.write(f"You have registered.\n".encode())
                
                elif arg[0] == 'who' and len(arg) == 1:
                    who_list = []
                    # who — просмотр зарегистрированных пользователей
                    for i in clients:
                        if clients[i].name:
                            who_list.append(clients[i].name)
                    writer.write(f'{"\n".join(who_list)}\n'.encode())
                
                elif arg[0] == 'cows' and len(arg) == 1:
                    cow_list = [i for i in cowsay.list_cows() if i not in clients.keys()]
                    # cows — просмотр свободных имён коров
                    writer.write(f'{"\n".join(cow_list)}\n'.encode())  
                    
                elif arg[0] == 'quit' and len(arg) == 1:
                    # quit — отключиться
                    flag_quit = True
                    
                for out in clients.values():
                    if out is not clients[me]:
                        await out.put(f"{me} {q.result().decode().strip()}")
            elif q is receive:
                receive = asyncio.create_task(clients[me].queue.get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
        if flag_quit:
            break
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
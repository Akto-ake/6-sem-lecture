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
    me = Client()
    flag_quit = False
    me_peer = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me_peer)
    # clients[me] = Client()
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
                        await writer.drain()
                        break
                        
                    if name_cow not in cowsay.list_cows():
                        writer.write(f"Error. Unknown cow.\n".encode())
                        await writer.drain()
                        break
                    
                    clients[me].name = name_cow
                    writer.write(f"You have registered.\n".encode())
                    await writer.drain()
                
                elif arg[0] == 'who' and len(arg) == 1:
                    who_list = []
                    # who — просмотр зарегистрированных пользователей
                    for i in clients:
                        if clients[i].name:
                            who_list.append(clients[i].name)
                    writer.write(f'{"\n".join(who_list)}\n'.encode())
                    await writer.drain()
                
                elif arg[0] == 'cows' and len(arg) == 1:
                    cow_list = [i for i in cowsay.list_cows() if i not in clients.keys()]
                    # cows — просмотр свободных имён коров
                    writer.write(f'{"\n".join(cow_list)}\n'.encode())  
                    await writer.drain()
                    
                elif arg[0] == 'quit' and len(arg) == 1:
                    # quit — отключиться
                    flag_quit = True
                    break
                    
                elif arg[0] == 'say' and len(arg) >= 3:
                    # say название_коровы текст сообщения — послать сообщение пользователю название_коровы
                    name_c = arg[1]
                    message = " ".join(arg[2:])

                    if name_c not in clients:
                        writer.write("Error. No such user.\n".encode())
                        await writer.drain()
                        continue

                    await clients[name_c].queue.put(cowsay.cowsay(message, cow=me.name))
                    writer.write("Message sent.\n".encode())
                    await writer.drain()
                
                elif arg[0] == 'yield' and len(arg) >= 2:
                    # yield текст сообщения — послать сообщение всем зарегистрированным пользователям
    
                    message = " ".join(arg[1:])
                    for name, client in clients.items():
                        if name != me.name:
                            await client.queue.put(cowsay.cowsay(message, cow=me.name))
                else:
                    writer.write("Error. Unknown command.\n".encode())
                    await writer.drain()
                    
            elif q is receive:
                receive = asyncio.create_task(me.queue.get())
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
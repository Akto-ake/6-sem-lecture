import asyncio
import cowsay
import shlex

clients = {}


class Client:
    def __init__(self):
        self.name = None
        self.queue = asyncio.Queue()

def who():
    return [client.name for client in clients.values() if client.name is not None]

def cows():
    busy = who()
    return [name for name in cowsay.list_cows() if name not in busy]

def login(me, name):
    if clients[me].name is not None:
        return "1 You are already logged in."

    if name not in cows():
        return "1 This cow cannot be used. Call cows to see free names."

    clients[me].name = name
    return "1 Successful login."

async def send_list(lst, error_text, writer):
    if lst:
        writer.write(f"0 {' '.join(lst)}\n".encode())
    else:
        writer.write(f"1 {error_text}\n".encode())
    await writer.drain()

async def send_message(sender, receivers, text):
    for client in clients.values():
        if client.name in receivers:
            await client.queue.put(f"2 {sender} {text}")

async def chat(reader, writer):
    flag_quit = False
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)

    clients[me] = Client()

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].queue.get())

    while not reader.at_eof():
        done, pending = await asyncio.wait(
            [send, receive],
            return_when=asyncio.FIRST_COMPLETED
        )

        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                arg = shlex.split(q.result().decode())

                if not arg:
                    continue

                if (arg[0] == "login") and len(arg) == 2:
                    name_cow = arg[1]

                    busy_names = []
                    for client in clients.values():
                        if client.name is not None:
                            busy_names.append(client.name)

                    if name_cow in busy_names:
                        writer.write("1 Error. This name is already taken\n".encode())
                        await writer.drain()

                    elif name_cow not in cowsay.list_cows():
                        writer.write("1 Error. Unknown cow.\n".encode())
                        await writer.drain()

                    elif clients[me].name is not None:
                        writer.write("1 You have registered.\n".encode())
                        await writer.drain()

                    else:
                        clients[me].name = name_cow
                        writer.write("1 Successful login.\n".encode())
                        await writer.drain()

                elif arg[0] == "who" and len(arg) == 1:
                    who_list = []
                    for client in clients.values():
                        if client.name is not None:
                            who_list.append(client.name)

                    if who_list:
                        writer.write(f"0 {' '.join(who_list)}\n".encode())
                    else:
                        writer.write("1 Error. No such user.\n".encode())
                    await writer.drain()

                elif arg[0] == "cows" and len(arg) == 1:
                    used_names = []
                    for client in clients.values():
                        if client.name is not None:
                            used_names.append(client.name)

                    cow_list = [
                        cow for cow in cowsay.list_cows()
                        if cow not in used_names
                    ]

                    if cow_list:
                        writer.write(f"0 {' '.join(cow_list)}\n".encode())
                    else:
                        writer.write("1 No free names.\n".encode())
                    await writer.drain()

                elif arg[0] == "quit" and len(arg) == 1:
                    flag_quit = True
                    break

                elif arg[0] == "say" and len(arg) >= 3:
                    if clients[me].name is None:
                        writer.write("1 Login to send and receive messages.\n".encode())
                        await writer.drain()
                        continue

                    name_c = arg[1]
                    message = " ".join(arg[2:])

                    found = False
                    for client in clients.values():
                        if client.name == name_c:
                            await client.queue.put(f"2 {clients[me].name} {message}")
                            found = True
                            break

                    if not found:
                        writer.write("1 Error. No such user.\n".encode())
                        await writer.drain()

                elif arg[0] == "yield" and len(arg) >= 2:
                    if clients[me].name is None:
                        writer.write("1 Login to send and receive messages.\n".encode())
                        await writer.drain()
                        continue

                    message = " ".join(arg[1:])
                    for name, client in clients.items():
                        if name != me and client.name is not None:
                            await client.queue.put(f"2 {clients[me].name} {message}")

                else:
                    writer.write("1 Invalid command.\n".encode())
                    await writer.drain()

            elif q is receive:
                receive = asyncio.create_task(clients[me].queue.get())
                if clients[me].name is not None:
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
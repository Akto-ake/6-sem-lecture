import sys
import socket
import cmd
import threading
import readline
import cowsay
import time


class ChatCmd(cmd.Cmd):
    prompt = "cow chat> "

    def __init__(self, socket):
        super().__init__()
        self.s = socket
        self.waiting_completion = False
        self.response = []

    def do_who(self, args):
        self.s.sendall("who\n".encode())

    def do_cows(self, args):
        self.s.sendall("cows\n".encode())

    def do_login(self, args):
        self.s.sendall(f"login {args}\n".encode())

    def do_say(self, args):
        self.s.sendall(f"say {args}\n".encode())

    def do_yield(self, args):
        self.s.sendall(f"yield {args}\n".encode())

    def do_quit(self, args):
        self.s.sendall("quit\n".encode())
        return 1

    def do_EOF(self, args):
        self.s.sendall("quit\n".encode())
        return 1

    def default(self, args):
        print("Invalid command")

    def complete_login(self, text, line, begidx, endidx):
        if len((line[:endidx] + ".").split()) == 2:
            self.waiting_completion = True
            self.s.sendall("cows\n".encode())
            while self.waiting_completion:
                time.sleep(0.01)
            return [name for name in self.response if name.startswith(text)]

    def complete_say(self, text, line, begidx, endidx):
        if len((line[:endidx] + ".").split()) == 2:
            self.waiting_completion = True
            self.s.sendall("who\n".encode())
            while self.waiting_completion:
                time.sleep(0.01)
            return [name for name in self.response if name.startswith(text)]

    def get_message(self, cmdline, s):
        while response := s.recv(1024).decode():
            for line in response.splitlines():
                parts = line.split()
                if not parts:
                    continue

                if parts[0] == "0":
                    if self.waiting_completion:
                        self.response = parts[1:]
                        self.waiting_completion = False
                    else:
                        print(
                            f"\n{'\n'.join(parts[1:])}\n"
                            f"{cmdline.prompt}{readline.get_line_buffer()}",
                            end="",
                            flush=True
                        )

                elif parts[0] == "1":
                    if self.waiting_completion:
                        self.response = []
                        self.waiting_completion = False
                    else:
                        print(
                            f"\n{' '.join(parts[1:])}\n"
                            f"{cmdline.prompt}{readline.get_line_buffer()}",
                            end="",
                            flush=True
                        )

                elif parts[0] == "2":
                    sender = parts[1]
                    text = " ".join(parts[2:])
                    print(
                        f"\n{cowsay.cowsay(text, cow=sender)}\n"
                        f"{cmdline.prompt}{readline.get_line_buffer()}",
                        end="",
                        flush=True
                    )


if __name__ == "__main__":
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    cmdline = ChatCmd(socket=s)
    reader = threading.Thread(target=cmdline.get_message, args=(cmdline, s))
    reader.start()

    cmdline.cmdloop()

    s.shutdown(socket.SHUT_RDWR)
    s.close()
    reader.join()
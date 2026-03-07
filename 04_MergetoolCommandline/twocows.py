import cowsay
import cmd
import shlex

def res(first, second):
    first = first.split('\n')
    second = second.split('\n')

    if len(first) > len(second):
        second = [''] * (len(first) - len(second)) + second 
    else:
        first = [''] * (len(second) - len(first)) + first
    
    m_1 = 0
    for i in first:
        m_1 = max(m_1, len(i))

    m_2 = 0
    for i in second:
        m_2 = max(m_2, len(i))

    return '\n'.join([f'{a:<{m_1}} {b:<{m_2}}' for a, b in zip(first, second)])

class CowCmd(cmd.Cmd):
    """сommand line for cows :)"""
    prompt = ">"

    def do_list_cows(self, args):
        """just a list of all the characters"""
        print('\n'.join(cowsay.list_cows()))

    def do_make_bubble(self, args):
        """the text that the cow says"""
        print(cowsay.make_bubble(args))

    def do_cowsay(self, args):
        pass

    def do_cowthink(self, args):
        pass

    def do_EOF(self, args):
        return 1
    
if __name__ == "__main__":
    CowCmd().cmdloop()
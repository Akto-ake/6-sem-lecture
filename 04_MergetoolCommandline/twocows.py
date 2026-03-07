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
    """
    сommand line for cows :)
    acceptable parameters: '-e', '--eyes', '-T', '--tongue', '-W', '--width', '-c', '--character'
    and also: 'eyes=', 'tongue=', 'character=', 'width='

    """
    prompt = ">"

    def do_list_cows(self, args):
        """just a list of all the characters"""
        print('\n'.join(cowsay.list_cows()))

    def do_make_bubble(self, args):
        """the text that the cow says"""
        print(cowsay.make_bubble(args))

    def do_cowsay(self, args):
        """
        Rendering cows. You need to set parameters for the cow: character, words, eyes, language for first cow.
        And then "reply" and params for second cow.

        """

        args = shlex.split(args)

        reply_idx = args.index('reply')
        first = args[:reply_idx]
        second = args[reply_idx + 1:]

        name = 'default'
        eyes = cowsay.Option.eyes
        tongue = cowsay.Option.tongue
        width = 40
        message = ''

        for i in range(len(first)):
            word = first[i]
            if (word == '-e') or (word == '--eyes'):
                eyes = first[i + 1]
            elif (word.startswith('eyes=')):
                eyes = word[5:]
            elif (word == '-T') or (word == '--tongue'):
                tongue = first[i + 1]
            elif (word.startswith('tongue=')):
                tongue = word[7:]
            elif (word == '-c') or (word == '--character'):
                name = first[i + 1]
            elif (word.startswith('character=')):
                name = word[10:]
            elif (word == '-w') or (word == '--width'):
                width = int(first[i + 1])
            elif (word.startswith('width=')):
                width = word[6:]
            elif message == '': 
                message = word
        first = cowsay.cowsay(
            message,
            cow=name,
            eyes=eyes,
            tongue=tongue,
            width=width)

        name = 'default'
        eyes = cowsay.Option.eyes
        tongue = cowsay.Option.tongue
        width = 40
        message = ''

        for i in range(len(second)):
            word = second[i]
            if (word == '-e') or (word == '--eyes'):
                eyes = second[i + 1]
            elif (word.startswith('eyes=')):
                eyes = word[5:]
            elif (word == '-T') or (word == '--tongue'):
                tongue = second[i + 1]
            elif (word.startswith('tongue=')):
                tongue = word[7:]
            elif (word == '-c') or (word == '--character'):
                name = second[i + 1]
            elif (word.startswith('character=')):
                name = word[10:]
            elif (word == '-w') or (word == '--width'):
                width = int(second[i + 1])
            elif (word.startswith('width=')):
                width = word[6:]
            elif message == '': 
                message = word
        second = cowsay.cowsay(
            message,
            cow=name,
            eyes=eyes,
            tongue=tongue,
            width=width)
        print(res(first, second))

    def do_cowthink(self, args):
        args = shlex.split(args)

        reply_idx = args.index('reply')
        first = args[:reply_idx]
        second = args[reply_idx + 1:]

        name = 'default'
        eyes = cowsay.Option.eyes
        tongue = cowsay.Option.tongue
        width = 40
        message = ''

        for i in range(len(first)):
            word = first[i]
            if (word == '-e') or (word == '--eyes'):
                eyes = first[i + 1]
            elif (word.startswith('eyes=')):
                eyes = word[5:]
            elif (word == '-T') or (word == '--tongue'):
                tongue = first[i + 1]
            elif (word.startswith('tongue=')):
                tongue = word[7:]
            elif (word == '-c') or (word == '--character'):
                name = first[i + 1]
            elif (word.startswith('character=')):
                name = word[10:]
            elif (word == '-w') or (word == '--width'):
                width = int(first[i + 1])
            elif (word.startswith('width=')):
                width = word[6:]
            elif message == '': 
                message = word
        first = cowsay.cowthink(
            message,
            cow=name,
            eyes=eyes,
            tongue=tongue,
            width=width)

        name = 'default'
        eyes = cowsay.Option.eyes
        tongue = cowsay.Option.tongue
        width = 40
        message = ''

        for i in range(len(second)):
            word = second[i]
            if (word == '-e') or (word == '--eyes'):
                eyes = second[i + 1]
            elif (word.startswith('eyes=')):
                eyes = word[5:]
            elif (word == '-T') or (word == '--tongue'):
                tongue = second[i + 1]
            elif (word.startswith('tongue=')):
                tongue = word[7:]
            elif (word == '-c') or (word == '--character'):
                name = second[i + 1]
            elif (word.startswith('character=')):
                name = word[10:]
            elif (word == '-w') or (word == '--width'):
                width = int(second[i + 1])
            elif (word.startswith('width=')):
                width = word[6:]
            elif message == '': 
                message = word
        second = cowsay.cowthink(
            message,
            cow=name,
            eyes=eyes,
            tongue=tongue,
            width=width)
        print(res(first, second))

    def do_EOF(self, args):
        return 1


if __name__ == "__main__":
    CowCmd().cmdloop()

import argparse
from cowsay import cowsay, list_cows, Option

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


parser = argparse.ArgumentParser(description='program with two cows')

parser.add_argument('message1', default=None, type=str, help='text of first cow')
parser.add_argument('message2', default=None, type=str, help='text of second cow')

parser.add_argument('-l', action='store_true', help='list of cows')

parser.add_argument('-e', '--eyes', type=str, default=Option.eyes, help='eye for first cow')
parser.add_argument('-E', '--eyes2', type=str, default=Option.eyes, help='eye for second cow')

parser.add_argument('-T', '--tongue', type=str, default=Option.tongue, help='tongue string for first cow')
parser.add_argument('-W', '--width', type=int, default=40, help='width')

parser.add_argument('-n', action='store_true', help='dont wrap text for first cow')
parser.add_argument('-N', action='store_true', help='dont wrap text for second cow')

parser.add_argument('-f', '--file', type=str, default='default', help = 'first cow file')
parser.add_argument('-F', '--file2', type=str, default='default', help= 'second cow file')


args = parser.parse_args()

if args.l:
    print("\n".join(sorted(list_cows())))
else:
    first = cowsay(
        message = args.message1,
        cow=args.file,
        eyes=args.eyes,
        tongue=args.tongue,
        width=args.width,
        wrap_text=args.n,
    )

    second = cowsay(
        message = args.message2,
        cow=args.file2,
        eyes=args.eyes2,
        tongue=args.tongue,
        width=args.width,
        wrap_text=args.N,
    )


    print(res(first, second))

import random
import sys
import urllib.request
import cowsay


def bullscows(word, answer):
    bulls = 0
    cows = 0
    word = list(word)
    answer = list(answer)
    dict_word = {}
    dict_answ = {}

    if len(word) != len(answer):
        print("не та длина слова. переделывай.")
        return
    i = 0

    while i < (len(answer)):
        if word[i] == answer[i]:
            bulls += 1
            i += 1
            continue
        if word[i] in dict_word:
            dict_word[word[i]] += 1
        else:
            dict_word[word[i]] = 1
        
        if answer[i] in dict_answ:
            dict_answ[answer[i]] += 1
        else:
            dict_answ[answer[i]] = 1
        i += 1

    for k in dict_word:
        k_w = dict_word[k]
        k_ans =  dict_answ.get(k, 'NO')
        if k_ans == 'NO':
            continue
        cows += min(k_w, k_ans)
    return (bulls, cows)

# gameplay(ask: callable, inform: callable, words: list[str]) -> int — функция-приложение, обеспечивающая геймплей:
# Задумывает случайное слово из списка слов words: list[str]
def gameplay(ask: callable, inform: callable, words: list[str]):
    answer = random.choice(words)
    print("answer:", answer)
    count_ask = 0

    while True:
        word = ask("Введите слово: ", words)
        count_ask += 1
        b, c = bullscows(word, answer)
        inform("Быки: {}, Коровы: {}", b, c)
        if b == len(answer):
            return count_ask

# Спрашивает у пользователя слово с помощью функции ask("Введите слово: ", words)

# Выводит пользователю результат с помощью функции inform("Быки: {}, Коровы: {}", b, c)

# Если слово не отгадано, переходит к п. 1
# Если слово отгадано, возвращает количество попыток — вызовов ask()

# Свойства функции ask():
# ask(prompt: str, valid: list[str] = None) -> str
# Если необязательный параметр valid не пуст, допустим только ввод слова из valid, иначе спрашивает повторно

def ask(prompt: str, valid: list[str] = None):
    cowsay.ghostbusters(prompt)
    stroka = input()
    if not valid:
        return stroka
    while not stroka in valid:
        cowsay.ghostbusters(prompt)
        stroka = input()
    return stroka

# Функция inform():
# inform(format_string: str, bulls: int, cows: int) -> None

def inform(format_string: str, bulls: int, cows: int):
    cowsay.cow((format_string.format(bulls, cows)))

if len(sys.argv) == 2:
    len_word = 5
elif len(sys.argv) == 3:
    len_word = sys.argv[2]

    d = sys.argv[1]
    if d.startswith(('http://', 'https://')):
        d = urllib.request.urlopen(d).read().decode().split('\n')
    else:
        d = open(d).read().split('\n')
    d_end = []
    for i in d:
        if len(i) == int(len_word):
            d_end.append(i)

    if len(d_end) == 0:
        print("Нет слов. Дайте другой словарь")
    else:
        print(f"Слово отгадано! Вам потребовалось: {gameplay(ask, inform, d)} попыток.")
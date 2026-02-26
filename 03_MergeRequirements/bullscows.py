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
        # print(word, answer, word[i])
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
        
    # print(dict_word, dict_answ)
    return (bulls, cows)

# gameplay(ask: callable, inform: callable, words: list[str]) -> int — функция-приложение, обеспечивающая геймплей:
# Задумывает случайное слово из списка слов words: list[str]

# Спрашивает у пользователя слово с помощью функции ask("Введите слово: ", words)

# Выводит пользователю результат с помощью функции inform("Быки: {}, Коровы: {}", b, c)

# Если слово не отгадано, переходит к п. 1
# Если слово отгадано, возвращает количество попыток — вызовов ask()

# Свойства функции ask():
# ask(prompt: str, valid: list[str] = None) -> str
# Если необязательный параметр valid не пуст, допустим только ввод слова из valid, иначе спрашивает повторно

def ask(prompt: str, valid: list[str] = None):
    stroka = input(prompt)
    if not valid:
        return stroka
    while not stroka in valid:
        stroka = input(prompt)

# Функция inform():
# inform(format_string: str, bulls: int, cows: int) -> None

def inform(format_string: str, bulls: int, cows: int):
    print(format_string.format(bulls, cows))



print(bullscows("ропот", "полип"))

        
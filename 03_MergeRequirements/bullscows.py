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


print(bullscows("ропот", "полип"))

        
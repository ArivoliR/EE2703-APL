import re
def most_common_word(text):
    if text !=
    if not text:
        return "No words found"
    l = {}
    text = text.lower()
    #print(text)
    L = re.split(",| ", text)
    #print(L)
    for i in L:
        if i in l:
            l[i] += 1
        else:
            l[i] = 1
    #print(l)
    max = 0
    for i in l:
        if l[i] > max:
            max = l[i]
            word = i
            if word == '':
                return "No words found"
    return f"""'{word}'""" + ' ' + str(max)
#print(most_common_word("The quick brown fox jumps over the lazy dog"))




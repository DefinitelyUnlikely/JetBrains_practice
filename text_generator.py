from collections import defaultdict
import nltk
import random
from nltk.tokenize import WhitespaceTokenizer

with open(input(), "r", encoding="utf-8") as corpus:
    tokens = WhitespaceTokenizer().tokenize(corpus.read())
    trigram_list = list(nltk.trigrams(tokens))

    head_tail = defaultdict(dict)

    for head_one, head_two, tail in trigram_list:
        head = head_one, head_two
        head_tail[head].setdefault(tail, 0)
        head_tail[head][tail] += 1

    sentences = []
    while len(sentences) < 10:
        sentence = []
        i = "start"
        while i[0][0].islower() or i[0][-1] in [".", "!", "?"]:
            i = random.choice(list(head_tail.keys()))
        sentence.extend(i)  

        while len(sentence) < 5 or sentence[-1][-1] not in [".", "!", "?"]:
            i = sentence[-2], sentence[-1]
            tails = head_tail[i]  
            keys, values = list(tails.keys()), list(tails.values())
            i = random.choices(keys, values)[0]    
            sentence.append(i) 

        sentences.append(" ".join(sentence) + "\n")

    print("".join(sentences))

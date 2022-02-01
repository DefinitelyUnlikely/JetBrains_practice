from nltk.tokenize import WhitespaceTokenizer


with open(input(), "r", encoding="utf-8") as corpus:
    tokens = WhitespaceTokenizer().tokenize(corpus.read())
    print("Corpus statistics")
    print(f"All tokens: {len(tokens)}")
    print(f"Unique tokens: {len(set(tokens))}")

    while True:
        i = input()

        if i == "exit":
            break

        try:
            print(tokens[int(i)])

        except IndexError:
            print("Index Error. Please input an integer that is in the range of the corpus.")
        except TypeError:
            print("Type Error. Please input an integer.")
        except ValueError:
            print("Type Error. Please input an integer.")

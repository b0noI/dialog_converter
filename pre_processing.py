from sys import argv

from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer()


if __name__ == "__main__":
    fname = argv[1]
    with open(fname, errors='ignore') as f:
        lines = f.readlines()

    for l in lines:
        processed = " ".join(tknzr.tokenize(l.strip())).lower()
        if processed and processed.strip()[:-1] != ".":
            processed = "{} .".format(processed)
        print(processed)


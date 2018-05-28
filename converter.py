import nltk.data

from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split

FNAME = "movie_lines.txt"
LINE_SEP = " +++$+++ "
DEBUG = False

SENT_DETECTOR = nltk.data.load('tokenizers/punkt/english.pickle')

# Example of the lineId: L19690
def get_line_number_from_id(line_id):
    return int(line_id[-1:])

def parse_line(dialogs):
    result = [[], []]
    # Buffer of the stat machine.
    last_ch_id = None
    last_movie_id = None
    last_line = None
    last_line_number = None
    i = 0
    for j in range(0, len(dialogs)):
        i = len(dialogs) - j - 1
        line_id, character_id, movie_id, _, line_txt = dialogs[i].split(LINE_SEP)
        line_number = get_line_number_from_id(line_id)
        # If movie ID has changed, bufer of the stat machine need to be set to new dialog.
        if movie_id != last_movie_id:
            if DEBUG:
                print("Movie id have changed from {} to {}, dropping buffer.".format(last_movie_id, movie_id))
            last_ch_id = character_id
            last_movie_id = movie_id
            last_line = line_txt
            last_line_number = line_number
            continue
        # If lines are from different dialogs, buufer of the stat machine need to be set to new dialog.
        if abs(line_number - last_line_number) > 1:
            if DEBUG:
                print("Line number changed to more then 1 from {} to {}. Dropping buffer.".format(last_line_number, line_number))
            last_ch_id = character_id
            last_movie_id = movie_id
            last_line = line_txt
            last_line_number = line_number
            continue
        # If same characters appears 2+ times buffer need to be erased.
        if last_ch_id == character_id:
            if DEBUG:
                print("Same character({} == {}) speaking 2 times in row.".format(last_ch_id, character_id))
            last_ch_id = None
            last_movie_id = None
            last_line = None
            last_line_number = None
            continue
        else:
            if DEBUG:
                print("Looks like: same film ({} == {}), line only diff on 1 ({} = {} + 1), and characters are different ({} != {}). Saving"
                    .format(last_movie_id, movie_id, last_line_number, line_number, last_ch_id, character_id))
            result[0].append(last_line.lower())
            result[1].append(line_txt.lower())
            last_ch_id = None
            last_movie_id = None
            last_line = None
            last_line_number = None
            continue
    return result


def sent_based_filter(dialogs):
    result_l = []
    result_r = []
    def is_sents_valid(sents, current_index, already_found_big_sent):
        if current_index == len(sents):
            return True
        tokens = word_tokenize(sents[current_index])
        if len(tokens) <= 3:
            return is_sents_valid(sents, current_index + 1, already_found_big_sent)
        if already_found_big_sent:
            return False
        return is_sents_valid(sents, current_index + 1, True)
    def is_valid(text):
        sents = SENT_DETECTOR.tokenize(text.strip())
        return is_sents_valid(sents, 0, False)
    for i in range(0, len(dialogs[0])):
        l = dialogs[0][i]
        r = dialogs[1][i]
        l_processed = " ".join(SENT_DETECTOR.tokenize(l.strip()))
        r_processed = " ".join(SENT_DETECTOR.tokenize(r.strip()))
        if is_valid(l) and is_valid(r):
            result_l.append(l_processed)
            result_r.append(r_processed)

    return [result_l, result_r]

def write_dialogs(dialogs, file_prefix):
    size = len(dialogs[0])
    left_f = open(file_prefix + '.a'.format(size), 'w')
    right_f = open(file_prefix + '.b'.format(size), 'w')
    for i in range(0, len(dialogs[0])):
        if not dialogs[0][i].strip() or not dialogs[1][i].strip():
            continue 
        left_f.write(dialogs[0][i])
        right_f.write(dialogs[1][i])
    left_f.close()
    right_f.close()


if __name__ == "__main__":
    dialogs = None
    with open(FNAME, errors='ignore') as f:
        dialogs = f.readlines()

    result = parse_line(dialogs)

    if DEBUG:
        print("Amount of a dialogs before the filtering: {}".format(len(result[0])))

    result = sent_based_filter(result)

    if DEBUG:
        print("Amount of a dialogs after the filtering: {}".format(len(result[0])))

    train_a, test_a, train_b, test_b = train_test_split(result[0], result[1], test_size=0.05)
    train_dialogs = [train_a, train_b]
    test_dialogs = [test_a, test_b]
    write_dialogs(train_dialogs, "train")
    write_dialogs(test_dialogs, "test")

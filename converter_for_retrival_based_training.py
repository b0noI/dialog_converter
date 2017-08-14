import nltk.data

import random

FNAME = "movie_lines.txt"
LINE_SEP = " +++$+++ "
DEBUG = True

SENT_DETECTOR = nltk.data.load('tokenizers/punkt/english.pickle')


# Example of the lineId: L19690
def get_line_number_from_id(line_id):
    return int(line_id[-1:])


def parse_raw_dialogs(raw_dialogs):
    parsed_dialogs = list()
    one_parsed_dialog = ([], [])
    participants = set()
    # Buffer of the stat machine.
    last_ch_id = None
    last_movie_id = None
    last_line = None
    last_line_number = None
    i = 0

    for j in range(0, len(raw_dialogs)):
        i = len(raw_dialogs) - j - 1
        line_id, character_id, movie_id, _, line_txt = raw_dialogs[i].split(LINE_SEP)
        line_number = get_line_number_from_id(line_id)
        # If movie ID has changed, bufer of the stat machine need to be set to new dialog.
        if movie_id != last_movie_id:
            if DEBUG:
                print("Movie id have changed from {} to {}, dropping buffer.".format(last_movie_id, movie_id))
            last_ch_id = character_id
            last_movie_id = movie_id
            last_line = line_txt
            last_line_number = line_number
            parsed_dialogs.append(one_parsed_dialog)
            one_parsed_dialog = ([], [])
            participants = set()
            continue
        # If lines are from different dialogs, buffer of the stat machine need to be set to new dialog.
        if abs(line_number - last_line_number) > 1:
            if DEBUG:
                print("Line number changed to more then 1 from {} to {}. Dropping buffer.".format(last_line_number,
                                                                                                  line_number))
            last_ch_id = character_id
            last_movie_id = movie_id
            last_line = line_txt
            last_line_number = line_number
            parsed_dialogs.append(one_parsed_dialog)
            one_parsed_dialog = ([], [])
            participants = set()
            continue
        if last_ch_id == character_id:
            if DEBUG:
                print("Same character({} == {}) speaking 2 times in row."
                      " Lines will be concatenated.".format(last_ch_id, character_id))
            last_line = "{} . {}".format(last_line, line_txt)
            last_line_number = line_number
            last_movie_id = movie_id
            continue
        # 3 persons dialog, dropping the buffer without saving it
        if len(participants) == 2 and character_id not in participants:
            if DEBUG:
                print("Dropping buffer since there are more then 2 participants, already have: {} and the new is {}"
                      .format(str(participants), character_id))
            last_ch_id = character_id
            last_movie_id = movie_id
            last_line = line_txt
            last_line_number = line_number
            # parsed_dialogs.append(one_parsed_dialog)
            one_parsed_dialog = ([], [])
            participants = set()
        else:
            if DEBUG:
                print("Looks like: same film ({} == {}), lines from {} to {} to the same character, and next character"
                      " is different ({} != {}). Saving".format(last_movie_id, movie_id, last_line_number, line_number,
                                                                last_ch_id, character_id))
            if DEBUG:
                print("Size of q is: {}".format(len(one_parsed_dialog[0])))
            if character_id not in participants:
                participants.add(character_id)
            if len(one_parsed_dialog[1]) == 0 or not one_parsed_dialog[1][-1] == last_line.lower():
                one_parsed_dialog[0].append(last_line.lower())
                one_parsed_dialog[1].append(line_txt.lower())
            last_ch_id = character_id
            last_movie_id = movie_id
            last_line = line_txt
            last_line_number = line_number
            continue
    return parsed_dialogs


def write_dialogs(dialogs):
    with open("dialogs.raw", 'w') as foutput:
        for dialog in dialogs:
            if len(dialog[0]) > 0:
                for idx, question in enumerate(dialog[0]):
                    answer = dialog[1][idx]
                    foutput.write("Q: {}\nA: {}\n".format(question.replace('\n', ' . '), answer.replace('\n', ' . ')))
                foutput.write("###\n")


if __name__ == "__main__":
    raw_dialogs = None
    with open(FNAME, errors='ignore') as f:
        raw_dialogs = f.readlines()

    dialogs = parse_raw_dialogs(raw_dialogs)

    if DEBUG:
        print("Amount of a dialogs: {}".format(len(dialogs)))

    if DEBUG:
        dialogs_to_print = 5
        print("Printing random {} dialogs".format(dialogs_to_print))
        print("###")
        for _ in range(0, dialogs_to_print):
            idx = random.randint(0, len(dialogs) - 1)
            q, a = dialogs[idx]
            for idx, question in enumerate(q):
                answer = a[idx]
                print("Q: {}A: {}".format(question, answer))
            print("###")

    write_dialogs(dialogs)

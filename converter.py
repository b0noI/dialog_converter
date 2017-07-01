from sklearn.model_selection import train_test_split

FNAME = "movie_lines.txt"
LINE_SEP = " +++$+++ "
DEBUG = False

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
    with open(FNAME) as f:
        dialogs = f.readlines()

    result = parse_line(dialogs)

    if DEBUG:
        for i in range(0, len(result[0])):
            print ("FROM {}\n TO {}".format(result[0][i], result[1][i]))

    train_a, test_a, train_b, test_b = train_test_split(result[0], result[1], test_size=0.2)
    write_dialogs([train_a, train_b], "train")
    write_dialogs([test_a, test_b], "test")

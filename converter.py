FNAME = "movie_lines.txt"
LINE_SEP = " +++$+++ "
DEBUG = False


dialogs = None
with open(FNAME) as f:
    dialogs = f.readlines()

result = [[], []]

# Example of the lineId: L19690
def get_line_number_from_id(line_id):
    return int(line_id[-1:])

def parse_line():
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
            result[0].append(last_line)
            result[1].append(line_txt)
            last_ch_id = None
            last_movie_id = None
            last_line = None
            last_line_number = None
            continue

parse_line()

if DEBUG:
    for i in range(0, len(result[0])):
        print ("FROM {}\n TO {}".format(result[0][i], result[1][i]))

size = len(result[0])
left_f = open('train.a'.format(size),'w')
right_f = open('train.b'.format(size),'w')

for i in range(0, len(result[0])):
    left_f.write(result[0][i])
    right_f.write(result[1][i])

left_f.close()
right_f.close()

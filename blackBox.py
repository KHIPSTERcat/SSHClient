def get_logs(bb_filepath):
    HEADER_SIZE = 11
    TIME_STR_LEN = 8
    DATE_STR_LEN = 8
    FLAG_POS = 9
    LINE_END = '\r\n'
    logs = []
    with open(bb_filepath, 'r', encoding='utf-8') as bb_file:
        date = None
        line = bb_file.readline()
        while line != '':
            if len(line) < FLAG_POS:
                line = bb_file.readline()
                continue
            flag = line[FLAG_POS]
            if flag == '#':
                date = line[HEADER_SIZE:].rstrip(LINE_END)
                line = bb_file.readline()
            elif flag == 'w' or flag == 'e':
                time = line[:TIME_STR_LEN]
                content = line[HEADER_SIZE:].rstrip(LINE_END)
                next_line = bb_file.readline()
                while next_line != '' and next_line[FLAG_POS] == '>':
                    content += next_line[HEADER_SIZE:].rstrip(LINE_END)
                    next_line = bb_file.readline()
                logs.append([flag, date, time, content])
                line = next_line
            else:
                line = bb_file.readline()
    return logs

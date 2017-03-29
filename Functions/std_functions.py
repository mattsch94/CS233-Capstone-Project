import string

def split_string_by_100_char(stg):

    length = len(stg)
    cur_len = 0
    split_list = []

    while True:
        if cur_len + 100 >= length:
            split_list.append(stg[cur_len:])
            break
        else:
            split_list.append(stg[cur_len:cur_len+100])
            cur_len += 100

    return split_list

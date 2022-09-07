
buff_dic = {}
buff_option = {}

class buff:
    buff_name = ""
    buff_time = 0
    loop_count = -1
    child_list = []
    def __init__(self, buff_name, buff_time, loop_count):
        self.buff_name = buff_name
        self.buff_time = buff_time
        self.loop_count = loop_count

def insert(user_ID, buff_name, buff_time, loop_count):
    insert_buff = buff(buff_name, buff_time, loop_count)

    if user_ID in buff_dic:
        buff_dic[user_ID][buff_name] = insert_buff
    else:
        buff_dic[user_ID] = {buff_name:insert_buff}

    print("현재 누적 버프 상황")
    for key, value in buff_dic[user_ID].items():
        print(key, value.buff_name, value.buff_time, value.loop_count)

    return buff_dic[user_ID]

def erase(user_ID, buff_name):

    print("현재 누적 버프 상황")
    for key, value in buff_dic[user_ID].items():
        print(key, value.buff_name, value.buff_time, value.loop_count)

    if buff_name in buff_dic[user_ID]:
        del buff_dic[user_ID][buff_name]
        return 0
    else:
        return -1

def erase_all(user_ID):

    if user_ID in buff_dic:
        del buff_dic[user_ID]
        return 0
    else:
        return -1
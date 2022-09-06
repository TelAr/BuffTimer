
dic = {}

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

    return user_ID+','+buff_name+','+buff_time+','+loop_count
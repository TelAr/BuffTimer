import time
import asyncio
import discord
import buffManager
from discord.ext import commands

buff_info_dic = {}
buff_object_dic = {}
buff_option_dic = {}
buff_timer_dic = {}

class option:
    delay_time = 5

class buff:
    buff_name = ""
    buff_time = 0
    loop_count = -1
    child_list = []
    def __init__(self, buff_name, buff_time, loop_count):
        self.buff_name = buff_name
        self.buff_time = buff_time
        self.loop_count = loop_count

def state(server_ID ,user_ID):
    ID_pair = (server_ID, user_ID)
    if ID_pair in buff_info_dic:
        return buff_info_dic[ID_pair]
    else:
        return -1

def insert(server_ID, user_ID, buff_name, buff_time, loop_count):

    if (not buff_time.isdecimal()) or (not (loop_count.isdecimal() or (loop_count[0]=='-' and loop_count[1:].isdecimal()))):
        return -1
    elif buff_name=="":
        return -1

    buff_time = int(buff_time)
    loop_count = int(loop_count)

    if buff_time<=0:
        return -1

    insert_buff = buff(buff_name, buff_time, loop_count)

    ID_pair = (server_ID, user_ID)

    if ID_pair in buff_info_dic:
        buff_info_dic[ID_pair][buff_name] = insert_buff
    else:
        buff_info_dic[ID_pair] = {buff_name:insert_buff}

    print("현재 누적 버프 상황")
    for key, value in buff_info_dic[ID_pair].items():
        print(key, value.buff_name, value.buff_time, value.loop_count)

    return state(server_ID ,user_ID)

def erase(server_ID, user_ID, buff_name):

    ID_pair = (server_ID, user_ID)

    print("현재 누적 버프 상황")
    for key, value in buff_info_dic[ID_pair].items():
        print(key, value.buff_name, value.buff_time, value.loop_count)

    if buff_name in buff_info_dic[ID_pair]:
        del buff_info_dic[ID_pair][buff_name]
        return 0
    else:
        return -1

def erase_all(server_ID, user_ID):

    ID_pair = (server_ID, user_ID)

    if ID_pair in buff_info_dic:
        del buff_info_dic[ID_pair]
        return 0
    else:
        return -1

def option_info(server_ID, user_ID):

    ID_pair = (server_ID, user_ID)

    if ID_pair in buff_option_dic:
        return buff_option_dic[ID_pair]
    else:
        buff_option_dic[ID_pair] = option()
        return buff_option_dic[ID_pair]

def option_setting(server_ID, user_ID, index, value):

    ID_pair = (server_ID, user_ID)

    if index.isnumeric():
        index = int(index)
    else:
        return -1

    if not ID_pair in buff_option_dic:
        buff_option_dic[ID_pair] = option()

    if index == 1:
        buff_option_dic[ID_pair].delay_time=value
    else:
        return -1

async def run_coroutine(ctx):
    server_ID = ctx.guild.id
    user_ID = str(ctx.author)
    ID_pair = (server_ID, user_ID)

    print(user_ID+": run corutine")
    global_timer=60*60*4;

    buff_timer_dic[ID_pair]=global_timer

    while(buff_timer_dic[ID_pair]>0):
        print(buff_timer_dic[ID_pair])
        await asyncio.sleep(1)
        buff_timer_dic[ID_pair] -= 1

    return 0

def stop(ctx):
    server_ID = ctx.guild.id
    user_ID = str(ctx.author)
    ID_pair = (server_ID, user_ID)

    if ID_pair in buff_timer_dic and buff_timer_dic[ID_pair]>0:
        buff_timer_dic[ID_pair]=0;
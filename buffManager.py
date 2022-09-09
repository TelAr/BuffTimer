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

    if loop_count==0:
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

def init_buff_object(ID_pair):
    target_dic={}
    buff_object_dic[ID_pair] = target_dic

    for key in buff_info_dic[ID_pair]:
        info = buff_info_dic[ID_pair][key]
        actual_buff=buff(buff_name=info.buff_name, buff_time=info.buff_time, loop_count=info.loop_count)
        buff_object_dic[ID_pair][key]=actual_buff

async def tick(ctx):
    server_ID = ctx.guild.id
    user_ID = str(ctx.author)
    ID_pair = (server_ID, user_ID)
    message = ""
    kill_list = []

    for key in buff_object_dic[ID_pair]:
        object_buff = buff_object_dic[ID_pair][key]

        if (object_buff.loop_count == 0):
            kill_list.append(key)
            continue

        if object_buff.buff_time == buff_option_dic[ID_pair].delay_time:
            if message=="":
                message += object_buff.buff_name
            else:
                message += ", "+object_buff.buff_name

        object_buff.buff_time -= 1
        if(object_buff.buff_time==0):
            if object_buff.loop_count>0:
                object_buff.loop_count-=1
            object_buff.buff_time = buff_info_dic[ID_pair][key].buff_time

    for key in kill_list:
        del buff_object_dic[ID_pair][key]
    return message

async def run_coroutine(ctx):
    server_ID = ctx.guild.id
    user_ID = str(ctx.author)
    ID_pair = (server_ID, user_ID)

    if ID_pair in buff_timer_dic and buff_timer_dic[ID_pair]>0:
        print(user_ID + ": already run")
        return -1

    print(user_ID+": run corutine")
    init_buff_object(ID_pair)

    if not ID_pair in buff_option_dic:
        buff_option_dic[ID_pair] = option()

    global_timer=60*60*4;
    buff_timer_dic[ID_pair]=global_timer
    process_delay=0
    while(buff_timer_dic[ID_pair]>0):

        await asyncio.sleep(1)
        print(buff_timer_dic[ID_pair])

        if(len(buff_object_dic[ID_pair])==0):
            break
        message = await tick(ctx)
        buff_timer_dic[ID_pair] -= 1

        if message!="":
            message = str(ctx.author.mention)+"님의 "+message+" 버프가 앞으로 "+str(buff_option_dic[ID_pair].delay_time)+"초 만큼 남았어요!"
            await  ctx.send(message)

    buff_timer_dic[ID_pair] =0

    return 0

def stop(ctx):
    server_ID = ctx.guild.id
    user_ID = str(ctx.author)
    ID_pair = (server_ID, user_ID)

    if ID_pair in buff_timer_dic and buff_timer_dic[ID_pair]>0:
        buff_timer_dic[ID_pair]=0;
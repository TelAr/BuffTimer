import discord
import buffManager
import asyncio
from discord.ext import commands


def time_to_print(time):
    print_str = str(time) + "초 동안 지속"
    if time == 0:
        print_str = "무한히 지속"

    return print_str

def loop_to_print(loop):
    print_str = str(loop) + "번"
    if loop == 0:
        print_str = "무한히"

    return print_str

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all(), help_command = None)

@bot.event
async def on_ready():
    print('Loggend in Bot: ', bot.user.name)
    print('Bot id: ', bot.user.id)
    print('connection was succesful!')
    print('=' * 30)
@bot.command(aliases=['테스트', '안녕'])
async def hello(ctx):
    await ctx.send("{}, 안녕!".format(ctx.author.mention))

@bot.command(aliases=['입력'])
async def insert(ctx, buff_name ="", buff_time:int = -1, loop_count:int = -1):

#예외처리
    if str(type(buff_time)) != "<class 'int'>" or str(type(loop_count)) != "<class 'int'>":
        await ctx.send("버프 지속 시간이랑 반복 횟수는 정수형 숫자로 입력해주세요.")
        return

    if buff_name == "" or buff_time < 0:
        await ctx.send("버프 이름을 지정해주시거나 버프 시간을 입력해주세요. (버프 시간 0: 무한 지속)")
        return

    buff_list = buffManager.insert(user_ID=str(ctx.author), buff_name=buff_name, buff_time= buff_time, loop_count= loop_count)
#출력부
    buff_time_print = time_to_print(buff_time)
    loop_count_print = loop_to_print(loop_count)

    embed = discord.Embed(title="버프 입력", description="신규 입력 사항이에요!.", colour=0xFFFFFF)
    embed.add_field(name="{}의 현재 입력 사항".format(ctx.author), value=str(buff_name) + ": " + str(buff_time_print) + "되며 " + str(loop_count_print) + " 반복해요!", inline=False)

    print_list = ""
    for key in buff_list:

        value = buff_list[key]

        buff_time_print = time_to_print(value.buff_time)
        loop_count_print = loop_to_print(value.loop_count)

        print_list = print_list + str(value.buff_name) + ": " + str(buff_time_print) + "되며 " + str(loop_count_print) + " 반복해요!\n"

    embed.add_field(name="{}의 누적 입력 사항".format(ctx.author), value=print_list, inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['삭제'])
async def erase(ctx, buff_name=""):

    if buff_name=="":
        await ctx.send("버프 이름을 입력해주세요!")
        return
    flag = buffManager.erase(str(ctx.author), buff_name)

    if flag == 0:
        await ctx.send(str(ctx.author.mention)+"의 "+str(buff_name)+"(이)라는 버프가 삭제되었어요!")
    else:
        await ctx.send(str(ctx.author.mention) + "의 " + str(buff_name) + "(이)라는 이름의 버프는 없던거같아요....")

@bot.command(aliases=['전부삭제'])
async def erase_all(ctx):

    flag = buffManager.erase_all(str(ctx.author))

    if flag == 0:
        await ctx.send(str(ctx.author.mention)+"의 모든 버프가 삭제되었어요!")
    else:
        await ctx.send(str(ctx.author.mention) + "는 원래부터 버프가 없던거같아요....")

@bot.command(aliases=['도움', '도움말'])
async def help(ctx):
    embed = discord.Embed(title="명령어", description="이 봇이 사용 가능한 명령어들에요.", colour=0xFFFFFF)
    embed.add_field(name="!hello,\t!테스트,\t!안녕", value="안녕! 봇 작동 상태 확인 명령이에요.\n아무 응답도 없으면 죽은거같아요....", inline=False)
    embed.add_field(name="!help,\t!도움,\t!도움말", value="바로 이 페이지를 여는 명령이에요.\n이 문구를 보고 계신다면 사실 이미 아시는거죠!", inline=False)
    insert_info = "버프 내용을 입력하는 명령이에요.\n"
    insert_info = insert_info + "명령어 뒤에 버프 이름, 지속 시간, 희망하는 반복 횟수를 입력하면 되요.\n"
    insert_info = insert_info + "예를 들어 \"!insert 공격력증가 10 2\"라고 하면\n10초간 지속되는 공격력증가 버프를 2회 반복하겠다는 뜻이에요.\n"
    insert_info = insert_info + "특정 버프를 수정하실때도 동일하게 입력하시면 되요.\n"
    insert_info = insert_info + "버프 이름과 버프 지속 시간은 반드시 입력해주셔야 해요.\n"
    insert_info = insert_info + "반복횟수를 미입력하거나 음수로 입력 시 무한반복이 되요."
    embed.add_field(name="!insert,\t!입력\t(+ 버프 이름, 지속 시간(초), 반복 횟수)", value=insert_info, inline=False)
    erase_info = "입력된 버프를 삭제하는 명령이에요.\n"
    erase_info = erase_info + "명령어 뒤에 삭제하고 싶은 버프 이름을 입력하면 되요."
    embed.add_field(name="!erase,\t!삭제\t(+ 버프 이름)", value=erase_info, inline=False)
    embed.add_field(name="!erase_all,\t!전부삭제", value="사용자의 모든 버프를 날려버리는 명령어에요. 와장창!", inline=False)

    await  ctx.send(embed=embed)

#Token import
f=open("token", 'r')
tokenInfo = f.readline()
bot.run(tokenInfo)



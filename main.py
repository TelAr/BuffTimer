import discord
import buffManager
import asyncio
from discord.ext import commands


def time_to_print(time):
    print_str = str(int(time)) + "초 동안 지속"

    return print_str

def loop_to_print(loop):
    print_str = str(int(loop)) + "번"
    if int(loop) < 0:
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

    await ctx.send(str(ctx.guild)+"의 "+str(ctx.author.mention)+", 안녕!")

@bot.command(aliases=['입력'])
async def insert(ctx, buff_name ="", buff_time = "", loop_count = "-1"):

    print("입력 시작")
#예외처리
    buff_list = buffManager.insert(server_ID=ctx.guild.id, user_ID=str(ctx.author), buff_name=buff_name, buff_time= buff_time, loop_count= loop_count)

    if buff_list == -1:
        await ctx.send("잘못된 명령 입력이에요...")
        return

#출력부
    buff_time_print = time_to_print(buff_time)
    loop_count_print = loop_to_print(loop_count)

    embed = discord.Embed(title="버프 입력", description="신규 입력 사항이에요!.", colour=0xFFFFFF)
    embed.add_field(name="{}의 현재 입력 사항".format(ctx.author), value=str(buff_name) + ": " + str(buff_time_print) + "되며 " + str(loop_count_print) + " 실행해요!", inline=False)

    print_list = ""

    for key in buff_list:

        value = buff_list[key]

        buff_time_print = time_to_print(value.buff_time)
        loop_count_print = loop_to_print(value.loop_count)

        print_list = print_list + str(value.buff_name) + ": " + str(buff_time_print) + "되며 " + str(loop_count_print) + " 실행해요!\n"

    embed.add_field(name="{}의 누적 입력 사항".format(ctx.author), value=print_list, inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['상태'])
async def state(ctx):

    buff_list = buffManager.state(server_ID=ctx.guild.id, user_ID= str(ctx.author))
    if buff_list != -1:
        embed = discord.Embed(title="버프 상태", description="누적 입력 상태에요!", colour=0xFFFFFF)

        print_list = ""
        for key in buff_list:
            value = buff_list[key]

            buff_time_print = time_to_print(value.buff_time)
            loop_count_print = loop_to_print(value.loop_count)

            print_list = print_list + str(value.buff_name) + ": " + str(buff_time_print) + "되며 " + str(
                loop_count_print) + " 실행해요!\n"

        embed.add_field(name="{}의 누적 입력 사항".format(ctx.author), value=print_list, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(str(ctx.author.mention)+"는 버프가 아직 없는거같아요....")


@bot.command(aliases=['삭제'])
async def erase(ctx, buff_name=""):

    if buff_name=="":
        await ctx.send("버프 이름을 입력해주세요!")
        return
    flag = buffManager.erase(server_ID=ctx.guild.id, user_ID= str(ctx.author), buff_name= buff_name)

    if flag == 0:
        await ctx.send(str(ctx.author.mention)+"의 "+str(buff_name)+"(이)라는 버프가 삭제되었어요!")
    else:
        await ctx.send(str(ctx.author.mention) + "의 " + str(buff_name) + "(이)라는 이름의 버프는 없던거같아요....")

@bot.command(aliases=['전부삭제'])
async def erase_all(ctx):

    flag = buffManager.erase_all(server_ID=ctx.guild.id,user_ID= str(ctx.author))

    if flag == 0:
        await ctx.send(str(ctx.author.mention)+"의 모든 버프가 삭제되었어요!")
    else:
        await ctx.send(str(ctx.author.mention) + "는 원래부터 버프가 없던거같아요....")

@bot.command(aliases=['옵션'])
async def option(ctx):

    option_info = buffManager.option_info(server_ID=ctx.guild.id,user_ID= str(ctx.author))
    delay_time = option_info.delay_time

    embed = discord.Embed(title="옵션", description=str(ctx.author.mention)+"의 옵션 상태에요", colour=0xFFFFFF)
    embed.add_field(name="1. 사전 멘션 시간", value=str(delay_time)+"초\n주의사항: 버프 시간보다 사전 멘션 시간이 짧으면 멘션을 보낼 수 없어요....", inline=False)
    embed.set_footer(text="옵선 설정을 하고 싶을 경우 \'옵션설정\' 명령을 사용해보세요")
    await  ctx.send(embed=embed)

@bot.command(aliases=['옵션설정', '옵션세팅'])
async def option_setting(ctx, index, value):
    if buffManager.option_setting(server_ID=ctx.guild.id,user_ID= str(ctx.author), index=index, value= value) == -1:
        await ctx.send("잘못된 명령 입력이에요...")
    else:
        await ctx.send("옵션 설정이 완료되었어요!")

@bot.command(aliases=['실행'])
async def run(ctx):
    await ctx.send("실행 시작이에요!")
    await buffManager.run_coroutine(ctx)
    await ctx.send("실행 완료에요!")

@bot.command(aliases=['중단', '중지'])
async def stop(ctx):

    buffManager.stop(ctx)
    await ctx.send("중단했어요!")

@bot.command(aliases=['도움', '도움말'])
async def help(ctx):
    embed = discord.Embed(title="명령어", description="이 봇이 사용 가능한 명령어들에요.", colour=0xFFFFFF)
    embed.add_field(name="!hello,\t!테스트,\t!안녕", value="안녕! 봇 작동 상태 확인 명령이에요.\n아무 응답도 없으면 죽은거같아요....", inline=False)
    embed.add_field(name="!help,\t!도움,\t!도움말", value="바로 이 페이지를 여는 명령이에요.\n이 문구를 보고 계신다면 사실 이미 아시는거죠!", inline=False)
    insert_info = "버프 내용을 입력하는 명령이에요.\n"
    insert_info = insert_info + "명령어 뒤에 버프 이름, 지속 시간, 희망하는 실행 횟수를 입력하면 되요.\n"
    insert_info = insert_info + "예를 들어 \"!insert 공격력증가 10 2\"라고 하면\n10초간 지속되는 공격력증가 버프를 2회 실행하겠다는 뜻이에요.\n"
    insert_info = insert_info + "특정 버프를 수정하실때도 동일하게 입력하시면 되요.\n"
    insert_info = insert_info + "버프 이름과 버프 지속 시간은 반드시 입력해주셔야 해요.\n"
    insert_info = insert_info + "버프 지속 시간은 반드시 양의 정수여야 해요.\n"
    insert_info = insert_info + "실행횟수를 미입력하거나 음수로 입력 시 무한반복이 되요."
    embed.add_field(name="!insert,\t!입력\t(+ 버프 이름, 지속 시간(초), 반복 횟수)", value=insert_info, inline=False)
    erase_info = "입력된 버프를 삭제하는 명령이에요.\n"
    erase_info = erase_info + "명령어 뒤에 삭제하고 싶은 버프 이름을 입력하면 되요."
    embed.add_field(name="!erase,\t!삭제\t(+ 버프 이름)", value=erase_info, inline=False)
    embed.add_field(name="!erase_all,\t!전부삭제", value="사용자의 모든 버프를 날려버리는 명령어에요. 와장창!", inline=False)
    embed.add_field(name="!option,\t!옵션", value="현재 옵션 정보를 보여주는 명령이에요!", inline=False)
    option_setting_info = "옵션을 세팅해주는 명령이에요.\n"
    option_setting_info = option_setting_info + "index값은 \"옵션\" 명령 기준으로 되어있는 번호로 선택이 가능해요"
    embed.add_field(name="!option_setting,\t!옵션설정\t!옵션세팅\t(+ index, 변경할 값)", value=option_setting_info, inline=False)

    await  ctx.send(embed=embed)

#Token import
f=open("token", 'r')
tokenInfo = f.readline()
bot.run(tokenInfo)

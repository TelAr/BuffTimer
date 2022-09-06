import discord
import buffManager
import asyncio
from discord.ext import commands

# command_prefix 안에는 원하는 접두사를 넣어주면 된다.
# ex) !, / ....
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

    print("입력 " + str(ctx.author) +": " + buff_name + ", " + str(buff_time) + ", " + str(loop_count))

#예외처리
    if str(type(buff_time)) != "<class 'int'>" or str(type(loop_count)) != "<class 'int'>":
        await ctx.send("버프 지속 시간이랑 반복 횟수는 숫자로 입력해주세요.")
        return

    if buff_name == "" or buff_time < 0:
        await ctx.send("버프 이름을 지정해주시거나 버프 시간을 입력해주세요. (버프 시간 0: 무한 지속)")
        return

#출력부
    if loop_count == -1:
        loop_count = "무한"

    embed = discord.Embed(title="버프 입력", description="신규 입력 사항이에요!.", colour=0xFFFFFF)
    embed.add_field(name="{}의 버프 입력 사항".format(ctx.author), value=buff_name + ": " + str(buff_time) + "초 동안 지속되며 " + str(loop_count) + "번 반복해요!")
    await ctx.send(embed=embed)

@bot.command(aliases=['삭제'])
async def erase(ctx):
    await ctx.send("{} 버프 삭제에요!".format(ctx.author.mention))

@bot.command(aliases=['도움', '도움말'])
async def help(ctx):
    embed = discord.Embed(title="명령어", description="이 봇이 사용 가능한 명령어들에요.", colour=0xFFFFFF)
    embed.add_field(name="!hello,\t!테스트,\t!안녕", value="안녕! 봇 작동 상태 확인 명령이에요.\n아무 응답도 없으면 죽은거같아요....", inline=False)
    embed.add_field(name="!help,\t!도움,\t!도움말", value="바로 이 페이지를 여는 명령이에요.\n이 문구를 보고 계신다면 사실 이미 아시는거죠!", inline=False)
    insert_info = "버프 내용을 입력하는 명령이에요.\n"
    insert_info = insert_info + "명령어 뒤에 버프 이름, 버프 지속 시간, 희망하는 반복 횟수를 입력하면 되요.\n\n"
    insert_info = insert_info + "예를 들어 \"!insert 공격력증가 10 2\"라고 하면\n10초간 지속되는 공격력증가 버프를 2회 반복하겠다는 뜻이에요.\n"
    insert_info = insert_info + "반복횟수를 미입력하거나 음수로 입력 시 무한반복이 되요."
    embed.add_field(name="!insert,\t!입력", value=insert_info, inline=False)

    await  ctx.send(embed=embed)

#Token import
f=open("token", 'r')
tokenInfo = f.readline()
bot.run(tokenInfo)


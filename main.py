import discord
import asyncio
from discord.ext import commands

# command_prefix 안에는 원하는 접두사를 넣어주면 된다.
# ex) !, / ....
bot = commands.Bot(command_prefix='/',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Loggend in Bot: ', bot.user.name)
    print('Bot id: ', bot.user.id)
    print('connection was succesful!')
    print('=' * 30)
    # 위 코드는 =라는 문자를 30개 출력하라는 뜻이다.
@bot.command()
async def Hello(ctx):
    await ctx.send("{}, 안녕!".format(ctx.author.mention))

#Token import
f=open("token", 'r')
tokenInfo = f.readline()
bot.run(tokenInfo)


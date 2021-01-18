import discord
import random
import os
from discord.ext import commands

intents = discord.Intents.all()

c = commands.Bot(command_prefix = '!', intents=intents)
c.remove_command('help')

channels = []

@c.event
async def on_ready():
    print(f"{c.user.name}")

@c.event
async def on_member_join(member):
    bot_channel = discord.utils.get(member.guild.channels, name="הודעות-בוט")
    rand1 = random.randint(1,100)
    rand2 = random.randint(1,100)
    if rand1 == rand2:
        role = discord.utils.get(member.guild.roles, name="לג'נד")
        await member.add_roles(role)
    welcome_channel = discord.utils.get(member.guild.channels, name="מצטרפים")

    await welcome_channel.send(f"{member.mention} הצטרף")
    
    if(channel_already_exists(member.name)):
        await bot_channel.send(f"{member.mention} כבר יש חדר על שמך לכן אני לא אצור עוד אחד")
        return
    
    try:
        chann = await member.guild.create_voice_channel(member.name, type=discord.ChannelType.voice)
        await bot_channel.send(f"<@!{member.id}> יצרתי חדר בשמך")
        channels.append(chann)
    except:
        await channels[-1].delete()
        chann = await member.guild.create_voice_channel(member.name, type=discord.ChannelType.voice)
        await bot_channel.send(f"<@!{member.id}> יצרתי חדר בשמך")
        channels.append(chann)

@c.event
async def on_member_remove(member):
    bot_channel = discord.utils.get(member.guild.channels, name="הודעות-בוט")
    await bot_channel.send(f"<@!{member.id}> יצא מהשרת, אני מוחק את החדר שלו")
    for chan in channels:
        if member.name == chan.name:
            channels.remove(chan)
            await chan.delete()
    welcome_channel = discord.utils.get(member.guild.channels, name="מצטרפים")
    await welcome_channel.send(f"{member.mention} עזב")

def channel_already_exists(channel):
    for chan in channels:
        if channel == chan.name:
            return True
    return False

@c.command(intents=['helpme','עזרה','h'])
async def help(ctx):
    msg = """**פקודות**
    1. mention/mentionrandom/mr - מתייג מישהו רנדומלי מהשרת
    """

@c.command(intents=['mention','mr','m'])
async def mentionrandom(ctx):
    memberslist = ctx.message.guild.members
    rand = random.randint(1, len(memberslist))
    await ctx.messasge.channel.send(f"{memberslist[rand].mention} מתייג/ת אותך")
    
@c.command()
@commands.has_permissions(administrator = True)
async def setdelay(ctx, seconds: int):
    await ctx.message.delete()
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"שיניתי את הקולדאון ל{seconds} שניות",delete_after=3)

c.run(os.environ['DISCORD_TOKEN'])
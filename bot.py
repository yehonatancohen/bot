import discord
import random
import os
from discord.ext import commands

intents = discord.Intents.all()

c = commands.Bot(command_prefix = '.', intents=intents)
c.remove_command('help')

channels = []

@c.event
async def on_ready():
    print(f"{c.user.name}")

@c.command()
async def test(ctx):
    guild = ctx.message.guild
    category = await ctx.guild.create_category("יום סבבה")
    for i in range(1,50):
        chann = await guild.create_voice_channel('יום סבבה', type=discord.ChannelType.voice)
        await chann.edit(category=category)
    await ctx.message.channel.send("סיימתי ביץ")

@c.event
async def on_member_join(member):
    rand1 = random.randint(1,100)
    rand2 = random.randint(1,100)
    if rand1 == rand2:
        role = discord.utils.get(member.guild.roles, name="לג'נד")
        await member.add_roles(role)
    welcome_channel = discord.utils.get(member.guild.channels, name="מצטרפים")

    await welcome_channel.send(f"{member.mention} הצטרף")
    
    if(channel_already_exists(member.name)):
        bot_channel = discord.utils.get(member.guild.channels, name="הודעות-בוט")
        await bot_channel.send(f"{member.mention} כבר יש חדר על שמך לכן אני לא אצור עוד אחד")
        return
    
    try:
        chann = await member.guild.create_voice_channel(member.name, type=discord.ChannelType.voice)
        channels.append(chann)
    except:
        await channels[-1].delete()
        chann = await member.guild.create_voice_channel(member.name, type=discord.ChannelType.voice)
        channels.append(chann)

@c.event
async def on_member_remove(member):
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

c.run(os.environ['DISCORD_TOKEN'])
import discord
from discord.ext import commands
import os
import asyncio

bot = commands.Bot(command_prefix='p.',case_insensitive=True,description='A discord bot.',self_bot=False,owner_id=276043503514025984)

@bot.event
async def on_ready(ctx):
    print('Success!')

bot.run(os.environ.get('TOKEN'))

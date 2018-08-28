import discord
from discord.ext import commands
import os
import asyncio

bot = commands.Bot(command_prefix='p.',case_insensitive=True,description='A discord bot.',self_bot=False,owner_id=276043503514025984)
bot.remove_command('help')

def owner(ctx):
    return ctx.message.author.id == '276043503514025984'  # checks if @Pointless#1278 is the author of the command


@bot.event
async def on_ready(ctx):
    print('Success!')
    await bot.change_presence(game=discord.Game(name=f'over {len(bot.servers)} servers | ,help',type=3))


@bot.command(pass_context=True, aliases=['commands', 'cmds','h'])
async def help(ctx,cmd: str=None):
    '''Get the list of commands.\nUsage: !help [command]\nAliases: !commands, !cmds,!h\nPermissions: None'''
    if cmd == None:
        i = discord.Embed(title='Help', color=0xFFFF00)
        i.add_field(name='General', value='`help`')
        i.add_field(name='Informational', value='Nothing')
        i.add_field(name='Fun', value='')
        i.add_field(name='Utility', value='')
        i.add_field(name='Managing', value='')
        i.add_field(name='Moderation', value='')
        i.add_field(name='Owner', value='')
        i.set_footer(text='Do !help <command> to find out what it does.')
        await bot.say(embed=cmd)
    if cmd:
        get = bot.get_command(cmd)
        s = discord.Embed(title='Help', color=0xFFFF00)
        s.add_field(name=f'Command: ,{cmd}', value=f'Help: {get.help}')
        return await bot.say(embed=s)
    else:
        return

bot.run(os.environ.get('TOKEN'))

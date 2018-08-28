from discord.ext import commands
import asyncio
import inspect
import sys
import os

bot = commands.Bot(command_prefix='p.',case_insensitive=True,description='A discord bot.',self_bot=False,owner_id=276043503514025984)
bot.remove_command('help')

def owner(ctx):
    return ctx.message.author.id == '276043503514025984'  # checks if @Pointless#1278 is the author of the command


@bot.event
async def on_ready(ctx):
    print('Success!')
    await bot.change_presence(game=discord.Game(name=f'over {len(bot.servers)} servers | ,help',type=3))

@commands.check(owner)
@bot.command(pass_context=True,aliases=['evaluate'])
async def eval(ctx, *, code):
    '''Evaluate some code.\n`evaluate`'''
    code = code.strip('`')
    try:
        result = eval(code)
        if inspect.isawaitable(result):
            result = await result
        else:
            await bot.say('```py\nInput: {}\nOutput: {}\n```'.format(code, result))
    except Exception as e:
            await bot.say('```py\nInput: {}\n{}: {}```'.format(code, type(e).__name__, e))

@bot.command(pass_context=True, aliases=['commands', 'cmds','h'])
async def help(ctx,cmd: str=None):
    '''Get a list of commands.\n`commands` `cmds` `h`'''
    if cmd == None:
        i = discord.Embed(title='Help', color=0xFFFF00)
        i.add_field(name='General', value='`help`')
        i.add_field(name='Informational', value='Nothing')
        i.add_field(name='Fun', value='Nothing')
        i.add_field(name='Utility', value='Nothing')
        i.add_field(name='Managing', value='Nothing')
        i.add_field(name='Moderation', value='Nothing')
        i.add_field(name='Owner', value='Nothing')
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

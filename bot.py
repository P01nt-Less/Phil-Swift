import discord
from discord import ext
from discord.ext import commands
import asyncio
import inspect
import json
import sys
import requests
import json
import random
import urllib
from random import randint
import os
import yarl
import io
import traceback
import datetime
import ast
import textwrap
import time
import aiohttp
from contextlib import redirect_stdout

bot = commands.Bot(command_prefix='p!',case_insensitive=True,description='A discord bot.',self_bot=False,owner_id=276043503514025984,fetch_offline_members=True)
bot.remove_command('help')
HEADERS = {'TRN-Api-Key': '7cf12d1d-cf9a-4bef-bc7d-38f74d721e33'}
@bot.event
async def on_ready():
    print('Success!')
    await bot.change_presence(activity=discord.Game(name=f'over {len(bot.guilds)} servers | p!help',type=3))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    get = bot.get_channel(513297881428525056)
    embed=discord.Embed(title=f'{discord.Guild.name}',description='I joined a server!',color=0x00FF00)
    embed.set_thumbnail(url=discord.Guild.icon_url)
    await get.send(embed=embed)
    try:
        hi=discord.Embed(title='Hello!',description='I am Phil Swift, a bot created by a Flex Fan.\n My prefix is p.\nThe help command is p.help\nThank you for inviting me to your server!',color=0x00FF00)
        hi.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        await guild.channels[0].send(embed=hi)
    except discord.Forbidden:
        pass
@bot.event
async def on_guild_leave(guild):
    get = bot.get_channel(513297881428525056)
    embed2=discord.Embed(title=f'{discord.Guild.name}',description='I left a server!',color=0xFF0000)
    embed2.set_thumbnail(url=discord.Guild.icon_url)
    await get.send(embed=embed2)

# Source: https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/mod.py
class BannedMember(commands.Converter):
    async def convert(self, ctx, arg):
        bans = await ctx.guild.bans()

        try:
            member_id = int(arg)
            user = discord.utils.find(lambda u: u.user.id == member_id, bans)
        except ValueError:
            user = discord.utils.find(lambda u: str(u.user) == arg, bans)

        if user is None:
            return None

        return user
class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
        else:
            can_execute = ctx.author.id == ctx.bot.owner_id or \
                          ctx.author == ctx.guild.owner or \
                          ctx.author.top_role > m.top_role

            if not can_execute:
                raise commands.BadArgument('You cannot do this action on this user due to role hierarchy.')
            return m.id
class BannedMember(commands.Converter):
    async def convert(self, ctx, argument):
        ban_list = await ctx.guild.bans()
        try:
            member_id = int(argument, base=10)
            entity = discord.utils.find(lambda u: u.user.id == member_id, ban_list)
        except ValueError:
            entity = discord.utils.find(lambda u: str(u.user) == argument, ban_list)

        if entity is None:
            raise commands.BadArgument("Not a valid previously-banned member.")
        return entity

class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = f'{ctx.author} (ID: {ctx.author.id}): {argument}'

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(f'reason is too long ({len(argument)}/{reason_max})')
        return ret


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

def get_syntax_error(e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

@bot.command(pass_context=True, hidden=True, name='eval')
async def _eval(ctx, *, body: str):
        """Evaluates a code"""
        _last_result = None

        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                _last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
@bot.command(pass_context=True, aliases=['commands', 'cmds','h'])
async def help(ctx,cmd: str=None):
    '''Get a list of commands.\n`commands` `cmds` `h`'''
    if cmd == None:
        e = discord.Embed(title='Help', color=0xFFFF00)
        e.add_field(name='General', value='`help` `ping` `info` `suggest`')
        e.add_field(name='Informational', value='`cryptocurrency` `calculate`')
        e.add_field(name='Fun', value='`coinflip` `8ball` `comic` `dog` `cat` `catfact`')
        e.add_field(name='Utility', value='`part` `roll` `serverinfo` `userinfo`')
        e.add_field(name='Managing', value='`giverole` `takerole`')
        e.add_field(name='Moderation', value='`kick` `ban` `unban` `softban` `channelmute` `channelunmute` `warn` `purge`')
        e.add_field(name='Owner', value='`say` `shutdown`')
        await ctx.send(embed=e)
    if cmd:
        get = bot.get_command(cmd)
        s = discord.Embed(title='Help', color=0xFFFF00)
        s.add_field(name=f'p.{cmd}', value=f'{get.help}')
        return await ctx.send(embed=s)
    else:
        return

@bot.command(pass_context=True)
async def say(ctx, *, text: str=None):
    '''Make the bot say something'''
    if ctx.message.author.id == 276043503514025984:
        await ctx.message.delete()
        return await ctx.send(text)
    else:
        embed = discord.Embed(title='Error', description=f'Our mighty lord and saviour Phil Swift is not upon us.', color=0xFF0000)
        embed.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['shutdown'])
async def restart(ctx):
    '''Stop and run the bot again.\n`shutdown`'''
    if ctx.message.author.id == 276043503514025984:
        embed = discord.Embed(title='Restart', description=f'Restarting...', color=0xFF0000)
        embed.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        await ctx.send(embed=embed)
        await bot.logout()
    else:
        embed = discord.Embed(title='Error', description=f'Our mighty lord and saviour Phil Swift is not upon us.', color=0xFF0000)
        embed.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=embed)

'''
:'######:::'########:'##::: ##:'########:'########:::::'###::::'##:::::::
'##... ##:: ##.....:: ###:: ##: ##.....:: ##.... ##:::'## ##::: ##:::::::
 ##:::..::: ##::::::: ####: ##: ##::::::: ##:::: ##::'##:. ##:: ##:::::::
 ##::'####: ######::: ## ## ##: ######::: ########::'##:::. ##: ##:::::::
 ##::: ##:: ##...:::: ##. ####: ##...:::: ##.. ##::: #########: ##:::::::
 ##::: ##:: ##::::::: ##:. ###: ##::::::: ##::. ##:: ##.... ##: ##:::::::
. ######::: ########: ##::. ##: ########: ##:::. ##: ##:::: ##: ########:
:......::::........::..::::..::........::..:::::..::..:::::..::........::        '''


@bot.command(pass_context=True, aliases=['latency', 'pong'])
async def ping(ctx):
    '''Find the response time in milliseconds.\n`latency` `pong`'''
    ptime = time.time()
    embed = discord.Embed(Title='Ping', color=0x00FF00)
    embed.add_field(name='Pong!', value='Calculating...')
    embed.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    ping3 = await ctx.send(embed=embed)
    ping2 = time.time() - ptime
    ping1 = discord.Embed(Title='Ping', color=0x00FF00)
    ping1.add_field(name='Pong!', value='{} milliseconds.'.format(int((round(ping2 * 1000)))))
    ping1.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ping3.edit(embed=ping1)

@bot.command(pass_context=True, aliases=['stats', 'statistics', 'information'])
async def info(ctx):
    '''Find information about the bot.\n`stats` `statistics` `information`'''
    sinfo = discord.Embed(title='Information', color=0x00FF00)
    sinfo.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    sinfo.add_field(name='Servers', value='{} servers.'.format(str(len(bot.guilds))))
    sinfo.add_field(name='Discord.py version', value='Version {}'.format(discord.__version__))
    sinfo.add_field(name='Active Threads', value='Active: {}'.format(threading.active_count()))
    sinfo.add_field(name='Links', value='[Support Server](https://discord.gg/JpnSpyg \"Support Server\")\n[Invite Link](https://discordapp.com/oauth2/authorize?client_id=484052296955592704&scope=bot&permissions=8 \"Invite Link\")')
    sinfo.add_field(name='Credits', value='Rapptz - Creating Discord.py\nPointless#1278 - Creator of Phil Swift\nVilgot#7447 - Helped me out a ton')
    sinfo.set_thumbnail(url = bot.user.avatar_url)
    await ctx.send(embed=sinfo)

@bot.command(pass_context=True,aliases=['idea','suggestion','ideas','suggestions'])
async def suggest(ctx, *,idea=None):
    '''Suggest something.\n`idea` `suggestion` `ideas` `suggestions`'''
    if idea==None:
        error=discord.Embed(title='Error',description='Specify a suggestion!',color=0xFF0000)
        error.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=error)
    embed=discord.Embed(description=idea,color=0x00ff80, timestamp = datetime.datetime.utcnow())
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=f"{ctx.author.guild}")
    xx = bot.get_channel(431850567204077580)
    x = await xx.send(embed=embed)
    await x.add_reaction("✅")
    await x.add_reaction("❌")
    success=discord.Embed(title='Suggestion',description='Thanks for suggesting an idea!',color=0x00FF00)
    success.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=success)

@bot.command(pass_context=True,aliases=['issue','bugs','issues'])
async def bug(ctx, *, issue=None):
    '''Report bugs and issues here.\n`issue` `bugs` `issues`'''
    if issue==None:
        error=discord.Embed(title='Error',description='Specify the issue!')
        error.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=error)
    embed=discord.Embed(description=issue,color=0x00ff80, timestamp = datetime.datetime.utcnow())
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=f"{ctx.author.guild}")
    xx = bot.get_channel(431850567204077580)
    await xx.send(embed=embed)
    success=discord.Embed(title='Bug',description='Thanks for issuing the bug!',color=0x00FF00)
    success.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=success)


'''
'####:'##::: ##:'########::'#######::'########::'##::::'##::::'###::::'########:'####::'#######::'##::: ##::::'###::::'##:::::::
. ##:: ###:: ##: ##.....::'##.... ##: ##.... ##: ###::'###:::'## ##:::... ##..::. ##::'##.... ##: ###:: ##:::'## ##::: ##:::::::
: ##:: ####: ##: ##::::::: ##:::: ##: ##:::: ##: ####'####::'##:. ##::::: ##::::: ##:: ##:::: ##: ####: ##::'##:. ##:: ##:::::::
: ##:: ## ## ##: ######::: ##:::: ##: ########:: ## ### ##:'##:::. ##:::: ##::::: ##:: ##:::: ##: ## ## ##:'##:::. ##: ##:::::::
: ##:: ##. ####: ##...:::: ##:::: ##: ##.. ##::: ##. #: ##: #########:::: ##::::: ##:: ##:::: ##: ##. ####: #########: ##:::::::
: ##:: ##:. ###: ##::::::: ##:::: ##: ##::. ##:: ##:.:: ##: ##.... ##:::: ##::::: ##:: ##:::: ##: ##:. ###: ##.... ##: ##:::::::
###: ##::. ##: ##:::::::. #######:: ##:::. ##: ##:::: ##: ##:::: ##:::: ##::::'####:. #######:: ##::. ##: ##:::: ##: ########:
....::..::::..::..:::::::::.......:::..:::::..::..:::::..::..:::::..:::::..:::::....:::.......:::..::::..::..:::::..::........::'''

@bot.command(pass_context=True, aliases=['cc'])
async def cryptocurrency(ctx, coin:str):
    '''Find out cryptocurrency rates.\n`cc`'''
    coin = coin.upper()
    r = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + str(coin) + '&tsyms=USD,EUR,GBP')
    json = r.json()
    cr = requests.get("https://www.cryptocompare.com/api/data/coinlist/")
    cjson = cr.json()
    if r.status_code == 200:
        if coin == None:
            ncryptocurrency = discord.Embed(title='Error', description='Specify the cryptocurrency symbol, not cryptocurreny name!', color=0xFF0000)
            ncryptocurrency.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            return await ctx.send(embed=ncryptocurrency)
        if coin:
            scryptocurrency = discord.Embed(title='Cryptocurrency', description='{}.'.format(cjson['Data'][str(coin)]['FullName']), color=0x00FF00)
            scryptocurrency.set_thumbnail(url=cjson['BaseImageUrl'] + cjson['Data'][str(coin)]['ImageUrl'])
            scryptocurrency.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            scryptocurrency.add_field(name='Price', value=json['DISPLAY'][str(coin)]['USD']['PRICE'] + '\n' + json['DISPLAY'][str(coin)]['EUR']['PRICE'] + '\n' + json['DISPLAY'][str(coin)]['GBP']['PRICE'])
            scryptocurrency.add_field(name='Highest Price Today', value=json['DISPLAY'][str(coin)]['USD']['HIGHDAY'] + '\n' + json['DISPLAY'][str(coin)]['EUR']['HIGHDAY'] + '\n' + json['DISPLAY'][str(coin)]['GBP']['HIGHDAY'])
            scryptocurrency.add_field(name='Lowest Price Today', value=json['DISPLAY'][str(coin)]['USD']['LOWDAY'] + '\n' + json['DISPLAY'][str(coin)]['EUR']['LOWDAY'] + '\n' + json['DISPLAY'][str(coin)]['GBP']['LOWDAY'])
            scryptocurrency.add_field(name='Last Updated', value=json['DISPLAY'][str(coin)]['USD']['LASTUPDATE'])
            scryptocurrency.add_field(name='Supply', value=json['DISPLAY'][str(coin)]['USD']['SUPPLY'])
            scryptocurrency.add_field(name='Algorithm', value=cjson['Data'][str(coin)]['Algorithm'])
            scryptocurrency.add_field(name='Proof Type', value=cjson['Data'][str(coin)]['ProofType'])
            scryptocurrency.add_field(name='Rank', value=cjson['Data'][str(coin)]['SortOrder'])
            scryptocurrency.set_footer(text='Cryptocurrency information by https://cryptocompare.com/!')
            return await ctx.send(embed=scryptocurrency)
        else:
            return
    else:
        rcryptocurrency = discord.Embed(title='Error', description='I could not access the API! Direct Message Pointless#1278 so this can be fixed! (You will be credited for finding it out!)', color=0xFF0000)
        rcryptocurrency.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rcryptocurrency)

@bot.command(pass_context=True, aliases=['math','c','calc'])
async def calculate(ctx,*, expression):
    '''Work out expressions and equations.\n`math` `c`'''
    r = requests.get('http://api.mathjs.org/v4/?expr=' + urllib.parse.quote_plus(expression))
    text = r.text
    if r.status_code == 200:
        if expression == None:
            ncalculate = discord.Embed(title='Error', description='Specify the expression!', color=0xFF0000)
            ncalculate.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            return await ctx.send(embed=ncalculate)
        if expression:
            scalculate = discord.Embed(title='Expression', description='{}'.format(expression), color=0x00FF00)
            scalculate.add_field(name='Answer', value='Your answer is: ' + text)
            scalculate.set_footer(text='Type p.calchelp for help')
            scalculate.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            return await ctx.send(embed=scalculate)
        else:
            return
    if r.status_code == 400:
        icalculate = discord.Embed(title='Error', description='That is an invalid expression!', color=0xFF0000)
        icalculate.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=icalculate)
    else:
        rcalculate = discord.Embed(title='Error', description='I could not access the API! Direct Message Pointless#1278 so this can be fixed! (You will be credited for finding it out!)', color=0xFF0000)
        rcalculate.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rcalculate)

@bot.command(pass_context=True,aliases=['ch'])
async def calchelp(ctx):
    success = discord.Embed(title='Success', description='Check your DMs!', color=0xFFFF00)
    calchelp1 = discord.Embed(title='Help', description='Help command for calculate.', color=0xFFFF00)
    calchelp1.add_field(name='Operators', value='`+` Add \n `-` Subtract \n `*` Multiply \n `/` Divide \n `%` Modulo \n `^` Power \n `!` Factorial \n `and` Logical And \n `not` Logical Not \n `or` Logical Or \n `xor` Logical Exclusive Or \n `=` Assignment \n `to`,`in` Convert Units \n `==` Equal \n `!=` Unequal \n `<` Smaller Than \n `>` Larger Than \n `<=` Smaller Than or Equal To \n `=>` Larger Than or Equal To \n `:` Range')
    calchelp2 = discord.Embed(title='Arithmetic Functions', description='`simplify(expr)` Simplify an expression tree.\n`abs(x)` Calculate the absolute value of a number. \n `add(x,y)` Add two or more values, x + y. \n `cbrt(x [, allRoots])` Calculate the cubic root of a value. \n `ceil(x)` Round a value towards plus infinity If x is complex, both real and imaginary part are rounded towards plus infinity.\n`cube(x)` Calculate the cubic root of a value. \n`divide(x,y)` Divide two values, x / y.\n`exp(x)` Calculate the exponent of a value. \n `expm1` Subtract 1 from Exponent \n `fix` Round values towards zero \n `floor` Round values towards minus infinity \n `gcd` Greatest Common Divisor \n `hypot` Hypotenusa of values \n `lcm` Least Common Multiple \n `log` Logarithm of a value to a base \n `log10` Logarithm of a value \n `log1p` Logarithm of a value + 1 \n `log2` Logarithm of a value to a base of two \n `mod` Modulus \n `multiply` Multiply values \n `norm` Norm of a value to vector or matrix \n `nthRoot` nth root of a value \n `nthRoots` nth roots of a value \n `pow` Power of a value to a value \n `round` Round a value to the nearest integer \n `sqrt` Square Root \n `square` Squared \n `subtract` Subtract Values \n `xgcd` Extended Greatest Common Divisor \n `arg` Argument of a complex value \n `conj` Conjugate of a complex value \n `im` Imaginary Part of a complex value \n `re` Real Part of a complex value \n`acos` Inverse Cosine \n`acosh` Hyperbolic arccos\n`acot` Inverse Cotangent \n `acoth` Hyperbolic Arccotangent \n `acoth` Hyperbolic arccotangent \n `acsc` Inverse cosecant \n `acsch` Hyperbolic arccosecant \n `asec` Inverse secant` \n `asech` Hyperbolic arcsecant \n `asin` Inverse Sine\n`atan` Inverse tangent\n`atan2` Inverse tangent with two arguments\n`atanh` Hyperbolic arctangent\n`cos` Cosine\n`cosh` Hyperbolic cosine\n`cot` Cotangent\n`coth` Hyperbolic cotangent\n`csch` Hyperbolic cosecant\n`sec` Secant\n`sech` Hyperbolic Secant\n`sin` Sine\n`sinh` Hyperbolic Sine\n`tan` Tangent\n`tanh` Hyperbolic Tangent', color=0xFFFF00)
    calchelp3 = discord.Embed(title='Tests', description='`isInteger(x)` Test whether a value is an integer number.\n`isNaN(x)` Test whether a value is NaN (not a number).\n`isNegative(x)` Test whether a value is negative: smaller than zero\n`isNumeric(x)` Test whether a value is an numeric value.\n`isPositive(x)` Test whether a value is positive: larger than zero.\n`isPrime(x)` Test whether a value is prime: has no divisors other than itself and one.\n`isZero(x)` Test whether a value is zero.',color=0xFFFF00)
    calchelp4 = discord.Embed(title='Constants', description='`e`,`E` Euler’s number, the base of the natural logarithm. `2.718281828459045`\n`i` Imaginary unit, defined as ii=-1. A complex number is described as a + bi, where a is the real part, and b is the imaginary part. `sqrt(-1)`\n`Infinity` Infinity, a number which is larger than the maximum number that can be handled by a floating point number. `Infinity`\n `LN2` Returns the natural logarithm of 2. `0.6931471805599453`\n`LN10` Returns the natural logarithm of 10.	`2.302585092994046`\n`LOG2E` Returns the base-2 logarithm of E.	`1.4426950408889634`\n`LOG10E` Returns the base-10 logarithm of E. `0.4342944819032518`\n`NaN` Not a number. `NaN`\n`null` Value null. `null`\n`phi` Phi is the golden ratio. Two quantities are in the golden ratio if their ratio is the same as the ratio of their sum to the larger of the two quantities. Phi is defined as (1 + sqrt(5)) / 2. `1.618033988749895`\n`pi`,`PI` The number pi is a mathematical constant that is the ratio of a circle\'s circumference to its diameter. `3.141592653589793`\n`SQRT1_2` Returns the square root of 1/2. `0.7071067811865476`\n`SQRT2` Returns the square root of 2. `1.4142135623730951`\n`tau` Tau is the ratio constant of a circle\'s circumference to radius, equal to 2 * pi. `6.283185307179586`\n`undefined` An undefined value. Preferably, use null to indicate undefined values. `undefined`\n `version` Returns the version number of math.js. For example `0.24.1`',color=0xFFFF00)
    user = ctx.message.author
    calchelp1.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    calchelp2.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    calchelp3.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    calchelp4.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    success.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=success)
    await user.send(embed=calchelp1)
    await user.send(embed=calchelp2)
    await user.send(embed=calchelp3)
    await user.send(embed=calchelp4)

@bot.command(pass_context=True, aliases=['bbc'])
async def news(ctx,number:int=0):
    '''Get top headlines.'''
    r = requests.get('https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=1707459031e54ca1b18a145e17e916b8')
    json = r.json()
    if json["status"] == "ok":
        scat = discord.Embed(title='News', description=json['articles'][number+1]['title'], color=0x00FF00)
        scat.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        scat.set_footer(text='News by https://newsapi.org/')
        return await ctx.send(embed=scat)
    else:
        rcat = discord.Embed(title='Error', description='I could not access the API! Direct Message Pointless#1278 so this can be fixed! (You will be credited for finding it out!)', color=0xFF0000)
        rcat.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rcat)
'''
'########:'##::::'##:'##::: ##:
 ##.....:: ##:::: ##: ###:: ##:
 ##::::::: ##:::: ##: ####: ##:
 ######::: ##:::: ##: ## ## ##:
 ##...:::: ##:::: ##: ##. ####:
 ##::::::: ##:::: ##: ##:. ###:
 ##:::::::. #######:: ##::. ##:
..:::::::::.......:::..::::..::
'''


@bot.command(pass_context=True,aliases=['cf'])
async def coinflip(ctx):
    '''Flip a coin and either get heads or tails.\n`cf`'''
    scoinflip = discord.Embed(title='Coinflip', description=random.choice(['Heads', 'Tails']), color=0xFF0000)
    scoinflip.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    return await ctx.send(embed=scoinflip)


@bot.command(pass_context=True, name='8ball', aliases=['8b', 'eb'])
async def eightball(ctx, question:str=None):
    '''Ask a question and let the magic eightball answer for you!\n`8b` `eb`'''
    if question == None:
        neightball = discord.Embed(title='Error', description='Specify the question!', color=0xFF0000)
        neightball.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=neightball)
    if '?' not in question:
        qeightball = discord.Embed(title='Error', description='That is invalid and not a question!', color=0xFF0000)
        qeightball.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=qeightball)
    else:
        seightball = discord.Embed(title='8ball', description=random.choice(['Signs point to yes.', 'Yes.', 'Without a doubt.', 'As I see it, yes.', 'You may rely on it.', 'It is decidedly so.', 'Yes - definitely.', 'It is certain.', 'Most likely.', 'Outlook good.', 'Reply hazy, try again.', 'Concentrate and ask again.', 'Better not tell you now.', 'Cannot predict now.', 'Ask again later.', 'My sources say no.', 'Outlook not so good.', 'Very doubtful.', 'My reply is no.', 'Don\'t count on it.']), color=0x00FF00)
        seightball.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=seightball)


@bot.command(pass_context=True, aliases=['xkcd','co'])
async def comic(ctx):
    '''Check out a random comic, with a total of 2013 comics!.\n`co`,`xkcd`'''
    r = requests.get(f'https://xkcd.com/{random.randint(1,2013)}/info.0.json')
    json = r.json()
    if r.status_code == 200:
        scomic = discord.Embed(title='Comic', description=str(json['title']), color=0x00FF00)
        scomic.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        scomic.set_image(url=json['img'])
        scomic.set_footer(text='Comics by https://xkcd.com/!')
        return await ctx.send(embed=scomic)
    else:
        rcomic = discord.Embed(title='Error', description='I could not access the API! Direct Message Pointless#1278 so this can be fixed! (You will be credited for finding it out!)', color=0xFF0000)
        rcomic.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rcomic)


@bot.command(pass_context=True)
async def dog(ctx):
    '''Check out a random cute or funny dog!'''
    r = requests.get('https://random.dog/woof.json')
    json = r.json()
    if r.status_code == 200:
        sdog = discord.Embed(title='Dog', description='A random cute dog!', color=0x00FF00)
        sdog.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        sdog.set_image(url=json['url'])
        sdog.set_footer(text='Dogs by https://random.dog/!')
        return await ctx.send(embed=sdog)
    else:
        rdog = discord.Embed(title='Error', description='I could not access the API! Direct Message Pointless#1278 so this can be fixed! (You will be credited for finding it out!)', color=0xFF0000)
        rdog.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rdog)

@bot.command(pass_context=True)
async def cat(ctx):
    '''Check out a random cute or funny cat!'''
    r = requests.get(f'https://api.thecatapi.com/v1/images/search')
    json = r.json()
    if r.status_code == 200:
        scat = discord.Embed(title='Cat', description='A random cute cat!', color=0x00FF00)
        scat.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        scat.set_image(url=json[0]['url'])
        scat.set_footer(text='Cats by https://thecatapi.com')
        return await ctx.send(embed=scat)
    else:
        rcat = discord.Embed(title='Error', description='I could not access the API! Direct Message Pointless#1278 so this can be fixed! (You will be credited for finding it out!)', color=0xFF0000)
        rcat.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rcat)

@bot.command(pass_context=True, aliases=['cfact'])
async def catfact(ctx):
    '''Get a random cat fact.'''
    r = requests.get('https://cat-fact.herokuapp.com/facts/random')
    json = r.json()
    if r.status_code == 200:
        scat = discord.Embed(title='Cat Fact', description=json['text'], color=0x00FF00)
        scat.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        scat.set_footer(text='Cat Facts by https://cat-fact.herokuapp.com')
        return await ctx.send(embed=scat)
    else:
        rcat = discord.Embed(title='Error', description='I could not access the API! Direct Message Pointless#1278 so this can be fixed! (You will be credited for finding it out!)', color=0xFF0000)
        rcat.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rcat)

@bot.command(pass_context=True, aliases=['mcserv'])
async def minecraftserver(ctx,server):
    '''Get a random cat fact.'''
    r = requests.get('https://api.mcsrvstat.us/2/' + server)
    json = r.json()
    embeed = discord.Embed(title='IP Address', description=str(json['ip']) + str(':') + str(json['port']), color=0x00FF00)
    if json['online']=='true':
        embeed.add_field(name='MOTD', value=json['motd']['clean'][0])
        embeed.add_field(name='Version', value=json['version'])
    embeed.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    embeed.set_footer(text='MC Server Info by https://mcservstat.us/')
    return await ctx.send(embed=embeed)

@bot.command(pass_context=True, aliases=['mcserv'])
async def fortnitedailyshop(ctx,server):
    '''Get a random cat fact.'''
    r = requests.get('https://fortnite-public-api.theapinetwork.com/prod09/store/get')
    json = r.json()
    embeed = discord.Embed(title='IP Address', description=str(json['ip']) + str(':') + str(json['port']), color=0x00FF00)
    if json['online']=='true':
        embeed.add_field(name='MOTD', value=json['motd']['clean'][0])
        embeed.add_field(name='Version', value=json['version'])
    embeed.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    embeed.set_footer(text='MC Server Info by https://mcservstat.us/')
    return await ctx.send(embed=embeed)


'''
'##::::'##:'########:'####:'##:::::::'####:'########:'##:::'##:
 ##:::: ##:... ##..::. ##:: ##:::::::. ##::... ##..::. ##:'##::
 ##:::: ##:::: ##::::: ##:: ##:::::::: ##::::: ##:::::. ####:::
 ##:::: ##:::: ##::::: ##:: ##:::::::: ##::::: ##::::::. ##::::
 ##:::: ##:::: ##::::: ##:: ##:::::::: ##::::: ##::::::: ##::::
 ##:::: ##:::: ##::::: ##:: ##:::::::: ##::::: ##::::::: ##::::
. #######::::: ##::::'####: ########:'####:::: ##::::::: ##::::
:.......::::::..:::::....::........::....:::::..::::::::..:::::
'''


@bot.command(pass_context=True)
async def part(ctx, *choice):
    '''Take a letter out of any word!'''
    spart = discord.Embed(title='Part', description=str(random.choice(*choice)), color=0x00FF00)
    spart.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    return await ctx.send(embed=spart)

@bot.command(pass_context=True)
async def roll(ctx, maxnumber:int=6):
    '''Roll a dice, with a custom maximum number!'''
    if maxnumber == None:
        nroll = discord.Embed(title='Error', description=f'Specify a maximum number!', color=0xFF0000)
        nroll.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=nroll)
    sroll = discord.Embed(title='Roll', description=f'You rolled a {random.randint(1,maxnumber)}!', color=0x00FF00)
    sroll.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    return await ctx.send(embed=sroll)

@bot.command(pass_context=True,aliases=['si'])
async def serverinfo(ctx):
    '''See information about the server!\n`si`'''
    sserverinfo = discord.Embed(title = (str(ctx.message.guild.name)),colour=0x00FF00)
    sserverinfo.set_thumbnail(url = ctx.message.guild.icon_url)
    sserverinfo.add_field(name='Owner', value=str(ctx.message.guild.owner))
    sserverinfo.add_field(name ='ID', value=str(ctx.message.guild.id))
    sserverinfo.add_field(name ='Member Count', value=str(ctx.message.guild.member_count))
    sserverinfo.add_field(name ='Region', value=str(ctx.message.guild.region))
    sserverinfo.add_field(name ='AFK Timeout', value=str(ctx.message.guild.afk_timeout))
    sserverinfo.add_field(name ='AFK Channel', value=str(ctx.message.guild.afk_channel))
    sserverinfo.add_field(name ='Verification Level',value=str(ctx.message.guild.verification_level))
    sserverinfo.add_field(name ='Custom Emotes',value=len(ctx.message.guild.emojis))
    sserverinfo.add_field(name ='Channels',value=len(ctx.message.guild.channels))
    sserverinfo.add_field(name ='Features',value=str(ctx.message.guild.features))
    sserverinfo.set_footer(text =f'Created at: {str(ctx.message.guild.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"))}')
    await ctx.send(embed=sserverinfo)

@bot.command(pass_context=True,aliases=['ui'])
async def userinfo(ctx, user:discord.Member = None):
    '''See information about a user!\n`ui`'''
    if user is None:
        user = ctx.message.author
    suserinfo = discord.Embed(title = (str(user.display_name)),colour=0x00FF00)
    suserinfo.set_thumbnail(url = user.avatar_url_as(static_format='png',size=1024))
    suserinfo.add_field(name ='Joined at', value=str(user.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")))
    suserinfo.add_field(name ='Game Playing',value=str(user.activity.name))
    suserinfo.add_field(name ='Status',value=str(user.status))
    suserinfo.add_field(name ='Highest Role',value=str(user.top_role))
    suserinfo.set_footer(text =f'Created at: {str(user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"))}')
    await ctx.send(embed=suserinfo)
'''
'##::::'##::::'###::::'##::: ##::::'###:::::'######:::'####:'##::: ##::'######:::
 ###::'###:::'## ##::: ###:: ##:::'## ##:::'##... ##::. ##:: ###:: ##:'##... ##::
 ####'####::'##:. ##:: ####: ##::'##:. ##:: ##:::..:::: ##:: ####: ##: ##:::..:::
 ## ### ##:'##:::. ##: ## ## ##:'##:::. ##: ##::'####:: ##:: ## ## ##: ##::'####:
 ##. #: ##: #########: ##. ####: #########: ##::: ##::: ##:: ##. ####: ##::: ##::
 ##:.:: ##: ##.... ##: ##:. ###: ##.... ##: ##::: ##::: ##:: ##:. ###: ##::: ##::
 ##:::: ##: ##:::: ##: ##::. ##: ##:::: ##:. ######:::'####: ##::. ##:. ######:::
..:::::..::..:::::..::..::::..::..:::::..:::......::::....::..::::..:::......::::    '''


@bot.command(pass_context=True, aliases=['gr'])
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, member: discord.Member, *, role: discord.Role=None):
    '''Give a role to someone\nUsage: !giverole <member> <role>\nAliases: !gr\nPermissions: Manage Roles'''
    if not member:
        mgiverole = discord.Embed(title='Error', description='You must specify a member!', color=0xFF0000)
        mgiverole.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=mgiverole)
    if not role:
        rgiverole = discord.Embed(title='Error', description='You must specify a role!', color=0xFF0000)
        rgiverole.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rgiverole)
    if role not in ctx.message.guild.roles:
        ngiverole = discord.Embed(title='Error', description='That isn\'t a role!', color=0xFF0000)
        ngiverole.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=ngiverole)
    if role == None:
        nogiverole = discord.Embed(title='Error', description='That isn\'t a role!', color=0xFF0000)
        nogiverole.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=nogiverole)
    try:
        await member.add_roles(role)
        sgiverole = discord.Embed(title='Giverole', description=f'{ctx.message.author.mention} has given the role, {role}, to {member.name}!', color=0x00FF00)
        sgiverole.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        await ctx.send(embed=sgiverole)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            egiverole = discord.Embed(title='Error', description='The person you are trying to give a role to has high permissions.', color=0xFF0000)
            egiverole.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            return await ctx.send(embed=egiverole)
        elif 'FORBIDDEN (status code: 403): Missing Permissions' in str(e):
            egiverole = discord.Embed(title='Error', description='I don\'t have enough permissions! Try dragging my bot role above the role that you are using this command on. If that doesn\'t work, perhaps try giving my bot role more permissions or permissions related to that command.', color=0xFF0000)
            egiverole.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            return await ctx.send(embed=egiverole)
        else:
            await ctx.send(e)


@bot.command(pass_context=True, aliases=['tr'])
@commands.has_permissions(manage_roles=True)
async def takerole(ctx, member: discord.Member, *, role: discord.Role=None):
    '''Take a role away from someone\nUsage: !takerole <member> <role>\nAliases: !tr\nPermissions: Manage Roles'''
    if not member:
        mtakerole = discord.Embed(title='Error', description='You must specify a member!', color=0xFF0000)
        mtakerole.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=mtakerole)
    if not role:
        rtakerole = discord.Embed(title='Error', description='You must specify a role!', color=0xFF0000)
        rtakerole.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rtakerole)
    if role not in ctx.message.guild.roles:
        ntakerole = discord.Embed(title='Error', description='That isn\'t a role!', color=0xFF0000)
        ntakerole.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=ntakerole)
    await member.remove_roles(role)
    stakerole = discord.Embed(title='Takerole', description=f'{ctx.message.author.mention} has taken the role, {role}, from {member.name}!', color=0x00FF00)
    stakerole.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=stakerole)


'''
'##::::'##::'#######::'########::'########:'########:::::'###::::'########:'####::'#######::'##::: ##:
 ###::'###:'##.... ##: ##.... ##: ##.....:: ##.... ##:::'## ##:::... ##..::. ##::'##.... ##: ###:: ##:
 ####'####: ##:::: ##: ##:::: ##: ##::::::: ##:::: ##::'##:. ##::::: ##::::: ##:: ##:::: ##: ####: ##:
 ## ### ##: ##:::: ##: ##:::: ##: ######::: ########::'##:::. ##:::: ##::::: ##:: ##:::: ##: ## ## ##:
 ##. #: ##: ##:::: ##: ##:::: ##: ##...:::: ##.. ##::: #########:::: ##::::: ##:: ##:::: ##: ##. ####:
 ##:.:: ##: ##:::: ##: ##:::: ##: ##::::::: ##::. ##:: ##.... ##:::: ##::::: ##:: ##:::: ##: ##:. ###:
 ##:::: ##:. #######:: ########:: ########: ##:::. ##: ##:::: ##:::: ##::::'####:. #######:: ##::. ##:
..:::::..:::.......:::........:::........::..:::::..::..:::::..:::::..:::::....:::.......:::..::::..::   '''


@bot.command(pass_context=True, aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member=None, *, reason : ActionReason=None):
    '''Kick someone.\nUsage: !kick <member> [reason]\nAliases: !k\nPermissions: Kick Members'''
    if not member:
        mkick = discord.Embed(title='Error', description='You must specify a member!', color=0xFF0000)
        mkick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=mkick)
    if not reason:
        rkick = discord.Embed(title='Error', description='You must specify a reason!', color=0xFF0000)
        rkick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rkick)
    try:
        await member.kick(reason=reason)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            ekick = discord.Embed(title='Error', description='The person you are trying to kick has high permissions.', color=0xFF0000)
            ekick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            return await ctx.send(embed=ekick)
        else:
            await ctx.send(e)
    skick = discord.Embed(title='Kick', description=f'{ctx.message.author.mention} has kicked {member.name}\n{reason}', color=0x00FF00)
    skick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=skick)
    message = discord.Embed(title='Kick', description=f'{ctx.message.author.mention} has kicked you from {ctx.guild.name}\n{reason}', color=0xFF0000,timestamp = datetime.datetime.utcnow())
    message.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    return await member.send(embed=message)

@bot.command(pass_context=True, aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member=None, *,  reason : ActionReason=None):
    '''Ban someone\nUsage: !ban <member> [reason]\nAliases: !b\nPermissions: Ban Members'''
    if not member:
        mkick = discord.Embed(title='Error', description='You must specify a member!', color=0xFF0000)
        mkick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=mkick)
    if not reason:
        rkick = discord.Embed(title='Error', description='You must specify a reason!', color=0xFF0000)
        rkick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rkick)
    try:
        await member.ban(reason=reason)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            ekick = discord.Embed(title='Error', description='The person you are trying to ban has high permissions.', color=0xFF0000)
            ekick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            return await ctx.send(embed=ekick)
        else:
            await ctx.send(e)
    skick = discord.Embed(title='Ban', description=f'{ctx.message.author.mention} has banned {member.name}\n{reason}', color=0x00FF00)
    skick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=skick)
    message = discord.Embed(title='Ban', description=f'{ctx.message.author.mention} has banned you from {ctx.guild.name}\n{reason}', color=0xFF0000,timestamp = datetime.datetime.utcnow())
    message.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    return await member.send(embed=message)

@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, member: BannedMember, *, reason: ActionReason = None):
        if reason is None:
            skick = discord.Embed(title='Error', description=f'Specify a reason!', color=0x00FF00)
            skick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            await ctx.send(embed=skick)
        await ctx.guild.unban(member.user, reason=reason)
        if member.reason:
            reeason = discord.Embed(title='Unban', description=f'Unbanned {member.user} (ID: {member.user.id})\nPreviously banned for: {member.reason}\n{reason}', color=0x00FF00)
            reeason.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            await ctx.send(embed=reeason)
        else:
            reeasson = discord.Embed(title='Unban', description=f'Unbanned {member.user} (ID: {member.user.id})\n{reason}', color=0x00FF00)
            reeasson.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            await ctx.send(embed=reeasson)#
        message = discord.Embed(title='Unban', description=f'{ctx.message.author.mention} has unbanned you from {ctx.guild.name}.\n{reason}', color=0xFF0000,timestamp = datetime.datetime.utcnow())
        message.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await member.send(embed=message)

@bot.command(pass_context=True, aliases=['sban', 'sb'])
@commands.has_permissions(ban_members=True)
async def softban(ctx, member : discord.Member=None, *,  reason : ActionReason=None):
    '''Ban then unban someone to remove all messages sent by the user within 7 days.\nUsage: !softban <member> [reason]\nAliases: !sban, !sb\nPermissions: Ban Members'''
    if not member:
        mkick = discord.Embed(title='Error', description='You must specify a member!', color=0xFF0000)
        mkick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=mkick)
    if not reason:
        rkick = discord.Embed(title='Error', description='You must specify a reason!', color=0xFF0000)
        rkick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rkick)
    try:
        await member.ban(reason=reason,delete_message_days=7)
        await member.unban(reason=reason)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            ekick = discord.Embed(title='Error', description='The person you are trying to softban has high permissions.', color=0xFF0000)
            ekick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            return await ctx.send(embed=ekick)
        else:
            await ctx.send(e)
    skick = discord.Embed(title='Softban', description=f'{ctx.message.author.mention} has softban {member.name}\n{reason}', color=0x00FF00)
    skick.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=skick)
    message = discord.Embed(title='Softban', description=f'{ctx.message.author.mention} has softbanned you from {ctx.guild.name}\n{reason}', color=0xFF0000,timestamp = datetime.datetime.utcnow())
    message.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    return await member.send(embed=message)

@bot.command(pass_context=True, aliases=['cmute', 'channelm', 'cm'])
@commands.has_permissions(manage_messages=True)
async def channelmute(ctx,member : discord.Member, channel, *, reason : ActionReason=None):
    '''Mute someone in a channel.\nUsage: !channelmute <member> [reason]\nAliases: !cmute, !channelm, !cm\nPermissions: Manage Messages'''
    if not member:
        mchannelmute = discord.Embed(title='Error', description='You must specify a member!', color=0xFF0000)
        mchannelmute.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=mchannelmute)
    if not reason:
        rchannelmute = discord.Embed(title='Error', description='You must specify a reason!', color=0xFF0000)
        rchannelmute.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rchannelmute)
    oveerwrite = discord.PermissionOverwrite()
    oveerwrite.send_messages = False
    if channel == None:
        channel = ctx.message.channel
    await abc.channel.set_permissions(member, overwrite=oveerwrite)
    schannelmute = discord.Embed(title='Channel Mute', description=f'{ctx.message.author.mention} has channelmuted {member.mention}\n{reason}', color=0x00FF00)
    schannelmute.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=schannelmute)
    message = discord.Embed(title='Channel Mute', description=f'{ctx.message.author.mention} has channelmuted you in {ctx.guild.name}\n{reason}', color=0xFF0000,timestamp = datetime.datetime.utcnow())
    message.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    return await member.send(embed=message)

@bot.command(pass_context=True, aliases=['unchannelmute','cumute', 'channelum', 'cunm', 'chum'])
@commands.has_permissions(manage_messages=True)
async def channelunmute(ctx, member : discord.Member, *,  reason : ActionReason=None):
    '''Unmute someone in a channel.\nUsage: !channelunmute <member> [reason]\nAliases: !cumute,!channelum,!cunm,!chum\nPermissions: Manage Messages'''
    if not member:
        mchannelmute = discord.Embed(title='Error', description='You must specify a member!', color=0xFF0000)
        mchannelmute.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=mchannelmute)
    if not reason:
        rchannelmute = discord.Embed(title='Error', description='You must specify a reason!', color=0xFF0000)
        rchannelmute.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rchannelmute)
    oveerwritee = discord.PermissionOverwrite()
    oveerwritee.send_messages = True
    channeeell = ctx.message.channel
    await channeeell.set_permissions(member, overwrite=oveerwritee)
    schannelmute = discord.Embed(title='Channelmute', description=f'{ctx.message.author.mention} has channelunmuted {member.mention}\n{reason}', color=0x00FF00)
    schannelmute.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=schannelmute)
    message = discord.Embed(title='Channel Mute', description=f'{ctx.message.author.mention} has channelunmuted you in {ctx.guild.name}\n{reason}', color=0xFF0000,timestamp = datetime.datetime.utcnow())
    message.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    return await member.send(embed=message)

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def warn(ctx, member : discord.Member, *, reason : ActionReason=None):
    '''Warn someone about doing something wrong!\nUsage: !warn <member> [reason]\nAliases: None\nPermissions: Kick Members'''
    if not member:
        mwarn = discord.Embed(title='Error', description='You must specify a member!', color=0xFF0000)
        mwarn.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=mwarn)
    if not reason:
        rwarn = discord.Embed(title='Error', description='You must specify a reason!', color=0xFF0000)
        rwarn.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rwarn)
    swarn = discord.Embed(title='Warn', description=f'{ctx.message.author.mention} has warned {member.mention}\n{reason}', color=0x00FF00)
    swarn.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=swarn)
    message = discord.Embed(title='Warn', description=f'{ctx.message.author.mention} has warned you in {ctx.guild.name}\n{reason}', color=0xFF0000,timestamp = datetime.datetime.utcnow())
    message.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    return await member.send(embed=message)

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount:int=None):
    '''Purge a number of messages!\nUsage: !purge <amount>\nAliases: None\nPermissions: Manage Messages'''
    if amount == None:
        apurge = discord.Embed(title='Error', description='You must specify an amount!', color=0xFF0000)
        apurge.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=apurge)
    await ctx.channel.purge(limit=amount+1)
    spurge = discord.Embed(title='Purge', description=f'{ctx.message.author.mention} has purged {amount} messages!', color=0x00FF00)
    spurge.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=spurge,delete_after=3.0)

bot.run('NTI0MjgxMjY5MzY2ODE2Nzg4.Dvlysw.p4hByInJnmC48LRm0-68227vbf4')

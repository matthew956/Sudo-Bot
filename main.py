import discord
import random
from discord.ext import commands, tasks
from itertools import cycle
import os


client = commands.Bot(command_prefix = '.')
status = cycle(['A Simple Bot for Discord', 'Sudo Bot.py, My prefix is "."'])

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('A Simple Bot for Discord'))
  print('Bot is ready.')
  
@tasks.loop(seconds=50)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency * 1000)} ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
  responses = ['It is certain.',
               'It is decidedly so.',
               'Without a doubt',
               'Yes - definitely.',
               'You may rely on it.',
               'As I see it, yes.',
               'Most likely.',
               'Outlook good.',
               'Yes.',
               'Signs point to yes.',
               'Reply hazy, try again.',
               'Ask again later',
               'Better not tell you now.',
               'Cannot predict now.',
               'Concentrate and ask again.',
               "Don't count on it.",
               'My reply is no.',
               'My sources say no.',
               'Very doubtful.'
  ]

  await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def faustao(ctx):
  await ctx.send('Oloko bixo!')

@client.command()
async def clear(ctx, amount=120):
  if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
    await ctx.channel.purge(limit=amount)
@clear.error
async def clear_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send('Sorry you are not allowed to use this command.')


@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
  if (ctx.message.author.permissions_in(ctx.message.channel).kick_members):
    await member.kick(reason=reason)
@kick.error
async def kick_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send('Sorry you are not allowed to use this command.')
  

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
  if (ctx.message.author.permissions_in(ctx.message.channel).ban_members):
    await member.ban(reason=reason)
@ban.error
async def ban_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send('Sorry you are not allowed to use this command.')

@client.command()
async def unban(ctx, *, member):
  if (ctx.message.author.permissions_in(ctx.message.channel).ban_members):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users: 
      user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f'Unbanned {user.name}#{user.discriminator}')

@unban.error
async def unban_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send('Sorry you are not allowed to use this command.')

@client.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv('TOKEN')) 
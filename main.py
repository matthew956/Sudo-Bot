import discord
import random
import json
from discord.ext import commands, tasks
from itertools import cycle
import os

client = discord.ext.commands.Bot(command_prefix = '.')
status = cycle(['A Simple Bot for Discord', 'Sudo Bot.py, My prefix is "."'])

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('A Simple Bot for Discord'))
  print('[LOGS] Bot is ready!')

@tasks.loop(seconds=50)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def ping(ctx): 
  await ctx.send(f'Pong! {round(client.latency * 1000)} ms')


@client.command(aliases=['8ball'])
async def _8ball(ctx, * , question):
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
async def trump(ctx):
  await ctx.send("Let's build a wall!")

@client.command()
async def creeper(ctx):
  await ctx.send("Awwwww man, so we back in the mine, got our pickaxe swinging from side to side, Side-side to side. This task, a grueling one hope to find some diamonds tonight, night, night.")
  
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

@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
  guild = ctx.guild
  mutedRole = discord.utils.get(guild.roles, name="Muted")

  if not mutedRole:
    mutedRole = await guild.create_role(name="Muted")

    for channel in guild.channels:
      await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

  await member.add_roles(mutedRole, reason=reason)
  await ctx.send(f"Muted {member.mention} for reason {reason}")
  await member.send(f"You were muted in the server {guild.name} for {reason}")

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
  guild = ctx.guild
  mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

  await member.remove_roles(mutedRole)
  await ctx.send(f"Unmuted {member.mention}")
  await member.send(f"You were muted in the server {guild.name}")

with open('reports.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users']=[]

@client.command(pass_context = True)
@commands.has_permissions(manage_roles = True, ban_members = True)
async def warn(ctx,user:discord.User,*reason:str):
  if not reason: 
    await ctx.send("Please provide a reason.")
    return
  reason = '  '.join(reason)
  for current_user in report['users']:
    if current_user['name'] == user.name:
      current_user['reasons'].append(reason)
      break
    else:
      report['users'].append({
      'name':user.name,
      'reasons': [reason,]
    })
    with open('reports.json','w+') as f:
      json.dump(report,f)

@client.command(pass_context = True)
async def warnings(ctx,user:discord.User):
  for current_user in report['users']:
    if user.name == current_user['name']:
      await ctx.send(f"{user.name} has been reported {len(current_user['reasons'])} times : {','.join(current_user['reasons'])}")
      break
  else:
    await ctx.send(f"{user.name} has never been reported")  

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv('TOKEN')) 

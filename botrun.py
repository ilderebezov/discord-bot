import datetime
import logging
import discord
from discord.ext import commands
import json
from config import settings

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, help_command=None)


@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@bot.command()
async def ban(ctx, member: discord.Member, *, reasons=None):
    await member.ban(reason=reasons)


@bot.command()
async def unban(ctx, user: discord.User):
    await ctx.guild.unban(user)


@bot.event
async def on_member_join(member):
  logging.basicConfig(filename='users_log.log', format='%(message)s', level=logging.INFO)
  logging.info('user: {0} has joined the channel at: {1}\n'.format(member.name, str(datetime.datetime.now())))


@bot.event
async def on_member_remove(member):
  logging.info('user: {0} has left the channel at: {1}\n'.format(member.name, str(datetime.datetime.now())))


@bot.command()
async def help(ctx):
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')


try:
    with open("users_level.json") as fp:
        users = json.load(fp)
except Exception:
    users = {}


def save_users():
    with open("users_level.json", "w+") as fp:
        json.dump(users, fp, sort_keys=True, indent=4)


def add_points(user: discord.User, points: int):
    id = user.id
    if id not in users:
        users[id] = {}
    users[id]["points"] = users[id].get("points", 0) + points
    print("{} now has {} total message".format(user.name, users[id]["points"]))
    print("{} now has {} level".format(user.name, float(users[id]["points"]) // float(20)))
    save_users()


def get_points(user: discord.User):
    id = user.id
    if id in users:
        return users[id].get("points", 0)
    return 0


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if message.content == '.level':
        level = float(get_points(message.author)) // float(20)
        msg = "You have {} level!".format(level)
        await message.channel.send('User {0} has level {1}'.format(message.author.name, level))
    add_points(message.author, 1)
bot.run(settings['token'])

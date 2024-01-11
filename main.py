import discord
from discord.ext import commands
import traceback
import sys
import json 
import os

#for database
import asyncpg
from asyncpg.pool import create_pool
import keep_alive

#try:
token = os.environ.get('token')
database_url = os.environ.get('database_url')
 
#except: 
'''
with open ('config/config.json', 'r') as f:
    config = json.load(f)
    token = config['token']
    prefix = config['prefix']
    database_url = config['DATABASE_URL']
'''




bot = commands.Bot() #defining bot prefix 

bot.remove_command('help')


async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(f"{database_url}")
    print("[/]DATABASE     | Connected")


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.idle, 
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"{prefix}help")
    )
    print("Bot online!")



with open ('modules/modules.json', 'r') as data:
    cog_data = json.load(data)
    slashextension = cog_data['slashExtension']


if __name__ == "__main__":
    for slashextensions in slashextension:
        try:
            bot.load_extension(slashextensions)
            print(f"[/] loaded | {slashextensions}")
        except:
            print(f'Error loading {slashextensions}', file=sys.stderr)
            traceback.print_exc()

bot.loop.run_until_complete(create_db_pool())
keep_alive.keep_alive()
bot.run(f"{token}")
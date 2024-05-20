import discord
from discord.ext import commands
import traceback
import sys
import json 
import os

#logging
from commands.ready.logging_config import setup_logging
logger = setup_logging()

#for database  
from commands.database.databaseCommands import create_pool

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


bot = discord.Bot() #defining bot prefix 

async def dbsetup():
    # Create database connection pool
    bot.pg_con = await create_pool(database_url)

    



@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.idle, 
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"Your shop")
    )
    logger.info("BOT Online!")



with open ('modules/modules.json', 'r') as data:
    cog_data = json.load(data)
    slashextension = cog_data['slashExtension']


if __name__ == "__main__":
    for slashextensions in slashextension:
        try:
            bot.load_extension(slashextensions)
            logger.info(f"[/] loaded | {slashextensions}")
        except:
            logger.error(f'Error loading {slashextensions}')
            traceback.print_exc()

bot.loop.run_until_complete(dbsetup())

bot.run(f"{token}")

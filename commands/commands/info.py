import discord
from discord.ext import commands
from discord.commands import Option, slash_command
import json
import psutil
import sys
import requests

with open ('./././config/emoji.json', 'r') as f:
	emojidata = json.load(f)



class slash_botInfo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(guild_ids=[864779702554984458,556197206147727391],description="BOT info.")
	async def info(
		self,
		ctx
	):
		cpuEmote = emojidata["cpu"]
		ramEmote = emojidata["ram"]
		storageEmote = emojidata["storage"]
		pythonEmote = emojidata["python"]
		codeEmote = emojidata["code"]
		supportEmote = emojidata["support"]

		servercount = str(len(self.bot.guilds))

		await ctx.response.defer()
		
		embed = discord.Embed(
			color = discord.Color.random(),
			description=f"""
			> {codeEmote} `PYCORD Version` - {discord.__version__}
			> {pythonEmote} `Py Version` - {sys.version_info[0]}
			> {cpuEmote} `CPU` -  {psutil.cpu_percent()}%
			> {storageEmote} `Storage` - {psutil.disk_usage('/')[3]}%
			> {ramEmote} `RAM` - {psutil.virtual_memory()[2]}%
			> {supportEmote} `Server Count` - {servercount}
			"""
		)
		await ctx.respond(embed=embed)

def setup(bot):
	bot.add_cog(slash_botInfo(bot))
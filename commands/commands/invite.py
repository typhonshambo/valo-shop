from urllib import response
import discord
from discord.ext import commands
from discord.commands import Option, slash_command
import json

with open ('././config/emoji.json', 'r') as f:
	emojidata = json.load(f)

with open ('././config/config.json', 'r') as f:
	data = json.load(f)
	guilds = data['guilds']


class INVITE(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.slash_command(description="Invite the BOT in your server", guild_ids=guilds)
	async def invite(
		self,
		ctx
	):
		await ctx.response.defer()
		embed= discord.Embed(
			color=discord.Color.red(),
			description="> Thanks for choosing me! You can invite me by clicking on the button given below"
		)
		view = discord.ui.View()
		view.add_item(discord.ui.Button(label='Invite', url='https://discord.com/api/oauth2/authorize?client_id=980918916211695717&permissions=139586816064&scope=bot%20applications.commands', style=discord.ButtonStyle.url, emoji=emojidata["invite"]))
		await ctx.respond(embed=embed, view=view)
		
	
	
def setup(client):
	client.add_cog(INVITE(client))
import discord
from discord.ext import commands
from discord.commands import Option, slash_command
import requests
from .utils.shopData import *
import json
import nest_asyncio

with open ('././config/emoji.json', 'r') as f:
	emojidata = json.load(f)

with open ('././config/config.json', 'r') as f:
	data = json.load(f)
	guilds = data['guilds']


class LOGIN(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(description="Link to your Valorant account")
	async def login(
		self,
		ctx,
		username: Option(str, "Enter your RIOT username", required=True),
		password: Option(str, "Enter your RIOT password", required=True)
	):
		await ctx.response.defer()
		nest_asyncio.apply()
		try:
			guild_id = str(ctx.guild.id)
			author_id = str(ctx.author.id)
			user = await self.bot.pg_con.fetchrow("SELECT * FROM shopDB WHERE user_id = $1", author_id)
			
			userData = username_to_data(username, password)
			if not user:
				
				await self.bot.pg_con.execute("INSERT INTO shopDB (guild_id, user_id, username, password, access_token, entitlements_token, ingameUserID, region) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)", guild_id, author_id, username, password, userData[0], userData[1], userData[2], userData[3])
				embed = discord.Embed(
					color = discord.Color.random(),
					description="> Successfully linked"
				)
				view = discord.ui.View()
				view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
				view.add_item(discord.ui.Button(label='Github', url='https://github.com/typhonshambo/valo-shop', style=discord.ButtonStyle.url, emoji=emojidata["github"]))
				await ctx.respond(embed=embed, view=view)
			
			if user:
				await self.bot.pg_con.execute("UPDATE shopDB SET username = $1, password = $2, region=$3, access_token=$4, entitlements_token=$5, ingameUserID=$6 WHERE user_id = $7",username, password, userData[3], userData[0], userData[1], userData[2],author_id)
				embed = discord.Embed(
					color = discord.Color.random(),
					description="> Successfully linked"
				)
				view = discord.ui.View()
				view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
				view.add_item(discord.ui.Button(label='Github', url='https://github.com/typhonshambo/valo-shop', style=discord.ButtonStyle.url, emoji=emojidata["github"]))
				await ctx.respond(embed=embed, view=view)
		except:
			embed= discord.Embed(
				color=discord.Color.red(),
				description="> Wrong Username or Password provided!"
			)
			view = discord.ui.View()
			view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
			view.add_item(discord.ui.Button(label='Github', url='https://github.com/typhonshambo/valo-shop', style=discord.ButtonStyle.url, emoji=emojidata["github"]))
			await ctx.respond(embed=embed, view=view)


def setup(client):
	client.add_cog(LOGIN(client))
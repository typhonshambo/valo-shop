import discord
from discord.ext import commands
from discord.commands import Option, slash_command
import requests
from .utils.shopData import *
import json

with open ('././config/config.json', 'r') as f:
	data = json.load(f)
	guilds = data['guilds']

class LOGIN(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(description="Link to your Valorant account", guild_ids=guilds)
	async def login(
		self,
		ctx,
		username: Option(str, "Enter your RIOT username", required=True),
		password: Option(str, "Enter your RIOT password", required=True),
		region: Option(str, "Enter your region", required=True)
	):
		await ctx.response.defer()
		try:
			guild_id = str(ctx.guild.id)
			author_id = str(ctx.author.id)
			user = await self.bot.pg_con.fetchrow("SELECT * FROM shopDB WHERE user_id = $1", author_id)
			
			userData = username_to_data(username, password)
			if not user:
				
				await self.bot.pg_con.execute("INSERT INTO shopDB (guild_id, user_id, username, password, region, access_token, entitlements_token, ingameUserID) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)", guild_id, author_id, username, password, region, userData[0], userData[1], userData[2])
				embed = discord.Embed(
					color = discord.Color.random(),
					description="> Successfully linked"
				)
				await ctx.respond(embed=embed)
			
			if user:
				await self.bot.pg_con.execute("UPDATE shopDB SET username = $1, password = $2, region=$3, access_token=$4, entitlements_token=$5, ingameUserID=$6 WHERE user_id = $7",username, password, region, userData[0], userData[1], userData[2],author_id)
				embed = discord.Embed(
					color = discord.Color.random(),
					description="> Successfully linked"
				)
				await ctx.respond(embed=embed)
		except:
			embed= discord.Embed(
                color=discord.Color.red(),
                description="> Wrong Username or Password provided!"
            )
			await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(LOGIN(client))
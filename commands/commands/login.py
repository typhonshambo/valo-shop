import discord
from discord.ext import commands
from discord.commands import Option, slash_command
import requests
from .utils.shopData import *
import json

#logger
from commands.ready.logging_config import setup_logging
logger = setup_logging()

#for database  
from commands.database.databaseCommands import fetch_user_data, insert_user_data, update_user_data


with open ('././config/emoji.json', 'r') as f:
	emojidata = json.load(f)

with open ('././config/config.json', 'r') as f:
	configdata = json.load(f)

class LOGIN(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.slash_command(description="Link to your Valorant account")
	@commands.cooldown(1, 120, commands.BucketType.user)
	async def login(
		self,
		ctx,
		username: Option(str, "Enter your RIOT username", required=True), # type: ignore
		password: Option(str, "Enter your RIOT password", required=True) # type: ignore
	):
		await ctx.response.defer(ephemeral=True)
		
		try:
			
			guild_id = str(ctx.guild.id)
			author_id = str(ctx.author.id)
			user = await fetch_user_data(self.client.pg_con, author_id)
			userData = await username_to_data(username, password)
			if not user:
				
				await insert_user_data(
					self.client.pg_con,
					guild_id, 
					author_id, 
					username, 
					password, 
					userData[0], 
					userData[1], 
					userData[2], 
					userData[3]
				)

				embed = discord.Embed(
					color = discord.Color.random(),
					description="> Successfully linked"
				)
				embed.set_footer(text=("After 1 hr you need to login again!"))
				view = discord.ui.View()
				view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
				view.add_item(discord.ui.Button(label='Donation', url=configdata['donation_url'], style=discord.ButtonStyle.url, emoji='💰'))
				await ctx.respond(embed=embed, view=view, ephemeral=True)
			
			if user:
			
				await update_user_data(
					self.client.pg_con,
					username, 
					password, 
					userData[3], 
					userData[0], 
					userData[1], 
					userData[2],
					author_id
				)
				embed = discord.Embed(
					color = discord.Color.random(),
					description="> Successfully linked!"
					
				)
				embed.set_footer(text=("After 1 hr you need to login again!"))

				view = discord.ui.View()
				view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
				view.add_item(discord.ui.Button(label='Donation', url=configdata['donation_url'], style=discord.ButtonStyle.url, emoji='💰'))
				await ctx.respond(embed=embed, view=view)

		except Exception as e:
			logger.error(f"Failed to login {ctx.author.id} : {e}")
			embed= discord.Embed(
				color=discord.Color.red(),
				description="> Wrong Username or Password provided!"
			)
			embed.set_footer(text=("Note : You can run this command only 1 times in 2 mins"))
			view = discord.ui.View()
			view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
			view.add_item(discord.ui.Button(label='Donation', url=configdata['donation_url'], style=discord.ButtonStyle.url, emoji='💰'))
			await ctx.respond(embed=embed, view=view)

	@commands.slash_command(description="Unlink to your Valorant account")
	async def logout(
		self,
		ctx
	):
		await ctx.response.defer(ephemeral=True)

		try:
			author_id = str(ctx.author.id)
			user = await self.client.pg_con.fetchrow("SELECT * FROM shopDB WHERE user_id = $1", author_id)
			if not user:
				embed= discord.Embed(
					color=discord.Color.red(),
					description="> Login to continue, use `/login`"
				)
				view = discord.ui.View()
				view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
				view.add_item(discord.ui.Button(label='Donation', url=configdata['donation_url'], style=discord.ButtonStyle.url, emoji='💰'))
				await ctx.respond(embed=embed, view=view)
			if user:
				await self.client.pg_con.fetchval(
					"DELETE FROM shopDB WHERE user_id = $1", 
					author_id
				)
				embed = discord.Embed(
						color = discord.Color.green(),
						description="> Successfully unlinked"
				)
				await ctx.respond(embed=embed)
		except:
			embed= discord.Embed(
				color=discord.Color.red(),
				description="> Login to continue, use `/login`"
			)
			view = discord.ui.View()
			view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
			view.add_item(discord.ui.Button(label='Donation', url=configdata['donation_url'], style=discord.ButtonStyle.url, emoji='💰'))
			await ctx.respond(embed=embed, view=view)



def setup(client):
	client.add_cog(LOGIN(client))
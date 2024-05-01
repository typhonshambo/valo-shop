import discord
from discord.ext import commands
import json 
from .utils.shopData import userBalance

with open ('./././config/emoji.json', 'r') as f:
	emojidata = json.load(f)

with open ('././config/config.json', 'r') as f:
	configdata = json.load(f)

class balance(commands.Cog):
	def __init__(self, client):
		self.client = client


	@commands.slash_command(description="Get your Balance")
	async def balance(
		self,
		ctx
	):
		vpEmote = emojidata["vp"]
		rpEmote = emojidata["rp"]
		await ctx.response.defer()
		try:
			
			author_id = str(ctx.author.id)
			user = await self.client.pg_con.fetchrow("SELECT * FROM shopDB WHERE user_id = $1", author_id)
			
			if user:
				entitlements_token = user["entitlements_token"]
				access_token = user["access_token"]
				user_id = user["ingameuserid"]
				region = user["region"]

				balance_data = userBalance(entitlements_token, access_token, user_id, region)
				embed = discord.Embed(
				color = discord.Color.random(),
				description=f"""
				> {vpEmote} `Valorant Points` - {balance_data[0]}
				> {rpEmote} `Radianite Points` - {balance_data[1]}
				"""
				)
				view = discord.ui.View()
				view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
				view.add_item(discord.ui.Button(label='Donation', url=configdata['donation_url'], style=discord.ButtonStyle.url, emoji='💰'))
				await ctx.respond(embed=embed, view=view)
			
			else:
				embed= discord.Embed(
					color=discord.Color.red(),
					description="> Login to continue, use `/login`"
				)
				await ctx.respond(embed=embed)
					

		except:
			embed= discord.Embed(
				color=discord.Color.red(),
				description="> Login to continue, use `/login`"
			)
			await ctx.respond(embed=embed)

def setup(client):
	client.add_cog(balance(client))
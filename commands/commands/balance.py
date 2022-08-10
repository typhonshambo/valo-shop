import discord
from discord.ext import commands
import json 
from .utils.shopData import userBalance

with open ('./././config/emoji.json', 'r') as f:
	emojidata = json.load(f)

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
		try:
			await ctx.response.defer()
			author_id = str(ctx.author.id)
			user = await self.client.pg_con.fetchrow("SELECT * FROM shopDB WHERE user_id = $1", author_id)
			
			if user:
				entitlements_token = user["entitlements_token"]
				access_token = user["access_token"]
				user_id = user["ingameuserid"]

				balance_data = userBalance(entitlements_token, access_token, user_id)
				embed = discord.Embed(
				color = discord.Color.random(),
				description=f"""
				> {vpEmote} `Valorant Points` - {balance_data[0]}
				> {rpEmote} `Radianite Points` - {balance_data[1]}
				"""
				)
				await ctx.respond(embed=embed)

		except:
			pass

def setup(client):
	client.add_cog(balance(client))
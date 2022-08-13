import discord
from discord.ext import commands
import json 
from .utils.shopData import getVersion,priceconvert,skins,check_item_shop




class itemshop(commands.Cog):
	def __init__(self, client):
		self.client = client


	@commands.slash_command(description="Get your Valorant Shop")
	async def shop(
		self,
		ctx
	):
		
		try:
			await ctx.response.defer()
			author_id = str(ctx.author.id)
			user = await self.client.pg_con.fetchrow("SELECT * FROM shopDB WHERE user_id = $1", author_id)
			
			if user:
				entitlements_token = user["entitlements_token"]
				access_token = user["access_token"]
				user_id = user["ingameuserid"]
				region = user["region"]

				skin_data = skins(entitlements_token, access_token, user_id, region)
				embed = discord.Embed(title=skin_data["bundle_name"], color=0x00FC7E)
				embed.set_image(url=skin_data["bundle_image"])
				await ctx.respond(embed=embed)
				try:
					embed = discord.Embed(title=f"{skin_data['skin1_name']} costs {skin_data['skin1_price']}", color=0x00FC7E)
					embed.set_image(url=skin_data["skin1_image"])
					await ctx.send(embed=embed)
					embed = discord.Embed(title=f"{skin_data['skin2_name']} costs {skin_data['skin2_price']}", color=0x00FC7E)
					embed.set_image(url=skin_data["skin2_image"])
					await ctx.send(embed=embed)
					embed = discord.Embed(title=f"{skin_data['skin3_name']} costs {skin_data['skin3_price']}", color=0x00FC7E)
					embed.set_image(url=skin_data["skin3_image"])
					await ctx.send(embed=embed)
					embed = discord.Embed(title=f"{skin_data['skin4_name']} costs {skin_data['skin4_price']}", color=0x00FC7E)
					embed.set_image(url=skin_data["skin4_image"])
					embed.set_footer(text=(f"Time Remaining : "+ str(skin_data['SingleItemOffersRemainingDurationInSeconds']) + skin_data['time_units']))
					await ctx.send(embed=embed)
				
				except:
					await ctx.respond("Loading complete!")
					pass
			
			else:
				embed= discord.Embed(
					color=discord.Color.red(),
					description="> Login to continue, use `/login`"
				)
				view = discord.ui.View()
				view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
				view.add_item(discord.ui.Button(label='Github', url='https://github.com/typhonshambo/valo-shop', style=discord.ButtonStyle.url, emoji=emojidata["github"]))
				await ctx.respond(embed=embed, view=view)

	
		except:
			embed= discord.Embed(
				color=discord.Color.red(),
				description="> Login to continue, use `/login`"
			)
			view = discord.ui.View()
			view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
			view.add_item(discord.ui.Button(label='Github', url='https://github.com/typhonshambo/valo-shop', style=discord.ButtonStyle.url, emoji=emojidata["github"]))
			await ctx.respond(embed=embed, view=view)






def setup(client):
	client.add_cog(itemshop(client))
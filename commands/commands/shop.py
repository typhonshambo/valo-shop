import discord
from discord.ext import commands
import json 
from .utils.shopData import skins

#logger
from commands.ready.logging_config import setup_logging
logger = setup_logging()

#for database  
from commands.database.databaseCommands import fetch_user_data

with open ('././config/emoji.json', 'r') as f:
	emojidata = json.load(f)

with open ('././config/config.json', 'r') as f:
	configdata = json.load(f)

class itemshop(commands.Cog):
	def __init__(self, client):
		self.client = client


	@commands.slash_command(description="Get your Valorant Shop")
	@commands.cooldown(2, 3600, commands.BucketType.user)
	async def shop(
		self,
		ctx
	):
		
		try:
			await ctx.response.defer()
			author_id = str(ctx.author.id)
			user = await fetch_user_data(self.client.pg_con, author_id)
		
			if user:
				entitlements_token = user["entitlements_token"]
				access_token = user["access_token"]
				user_id = user["ingameuserid"]
				region = user["region"]

				skin_data = skins(entitlements_token, access_token, user_id, region)
				embed = discord.Embed(title=skin_data["bundle_name"], description=f"> {emojidata['vp']} {skin_data['bundle_price']}", color=0x00FC7E)
				embed.set_image(url=skin_data["bundle_image"])
				await ctx.respond(embed=embed)
				try:
					embed = discord.Embed(title=f"{skin_data['skin1_name']}", description=f"> {emojidata['vp']} {skin_data['skin1_price']}",color=0x00FC7E)
					embed.set_image(url=skin_data["skin1_image"])
					await ctx.send(embed=embed)
					embed = discord.Embed(title=f"{skin_data['skin2_name']}",  description=f"> {emojidata['vp']} {skin_data['skin2_price']}",color=0x00FC7E)
					embed.set_image(url=skin_data["skin2_image"])
					await ctx.send(embed=embed)
					embed = discord.Embed(title=f"{skin_data['skin3_name']}", description=f"> {emojidata['vp']} {skin_data['skin3_price']}", color=0x00FC7E)
					embed.set_image(url=skin_data["skin3_image"])
					await ctx.send(embed=embed)
					embed = discord.Embed(title=f"{skin_data['skin4_name']}", description=f"> {emojidata['vp']} {skin_data['skin4_price']}", color=0x00FC7E)
					embed.set_image(url=skin_data["skin4_image"])
					embed.set_footer(text=(f"Time Remaining : "+ str(skin_data['SingleItemOffersRemainingDurationInSeconds']) + skin_data['time_units']))
					view = discord.ui.View()
					view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
					view.add_item(discord.ui.Button(label='Donation', url=configdata['donation_url'], style=discord.ButtonStyle.url, emoji='💰'))
					await ctx.send(embed=embed, view=view)


				except Exception as e:
					logger.warning(f"Failed to load shop {ctx.author.id} : {e}")
					await ctx.respond("Loading complete!")
					pass
			
			else:
				logger.error(f"Failed to load Creds {ctx.author.id} ")
				embed= discord.Embed(
					color=discord.Color.red(),
					description="> Login to continue, use `/login`"
				)
				embed.set_footer(text=("Note : You can run command only 2 times in 1 hour"))
				view = discord.ui.View()
				view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
				view.add_item(discord.ui.Button(label='Donation', url=configdata['donation_url'], style=discord.ButtonStyle.url, emoji='💰'))
				await ctx.respond(embed=embed, view=view)

	
		except Exception as e:
			logger.error(f"Failed to login {ctx.author.id} : {e}")
			embed= discord.Embed(
				color=discord.Color.red(),
				description="> Login to continue, use `/login`"
			)
			embed.set_footer(text=("Note : You can run command only 2 times in 1 hour"))
			view = discord.ui.View()
			view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
			view.add_item(discord.ui.Button(label='Donation', url=configdata['donation_url'], style=discord.ButtonStyle.url, emoji='💰'))
			await ctx.respond(embed=embed, view=view)






		
def setup(client):
	client.add_cog(itemshop(client))
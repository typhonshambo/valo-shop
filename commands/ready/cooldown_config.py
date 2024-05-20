import discord
from discord.ext import commands
import json

with open ('././config/emoji.json', 'r') as f:
	emojidata = json.load(f)

with open ('././config/config.json', 'r') as f:
	configdata = json.load(f)

class cooldownHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
		
	@commands.Cog.listener()
	async def on_application_command_error(self, ctx: commands.Context, error: commands.CommandError):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.response.defer(ephemeral=True)
			seconds = error.retry_after
			h, m, s = map(lambda x: int(x), [seconds/3600, seconds%3600/60, seconds%60])
			embed= discord.Embed(
				color=discord.Color.red(),
				description=f"> The Command is on cooldown!"
			)
			embed.set_footer(text=(f"Wait for {h}hr {m:02d}min {s:02d}seconds"))
			view = discord.ui.View()
			view.add_item(discord.ui.Button(label='Support Server', url='https://discord.gg/m5mSyTV7RR', style=discord.ButtonStyle.url, emoji=emojidata["support"]))
			view.add_item(discord.ui.Button(label='Donation', url=configdata['donation_url'], style=discord.ButtonStyle.url, emoji='💰'))
			await ctx.respond(embed=embed, view=view)
		else:
			raise error
	
def setup(bot):
	bot.add_cog(cooldownHandler(bot))
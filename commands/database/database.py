import discord
from discord.ext import commands

class database(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		print("[\] setting up DATABASE")
		
		#for leveling
		await self.bot.pg_con.execute("""
		CREATE TABLE IF NOT EXISTS shopDB
		(
			guild_id character varying,
			user_id character varying NOT NULL,
            username character varying,
            password character varying,
			region character varying,
			access_token character varying,
			entitlements_token character varying,
			ingameuserid character varying
		);
		""")
        

		


def setup(bot):
	bot.add_cog(database(bot))
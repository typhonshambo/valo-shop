import discord
from discord.ext import commands

from commands.ready.logging_config import setup_logging
logger = setup_logging()

class database(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		logger.info("setting up DATABASE")
		
		#for leveling
		try:
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
						
		
		except Exception as e:
			logger.error(f"Can't connect to DB : {e}")

        

		


def setup(bot):
	bot.add_cog(database(bot))
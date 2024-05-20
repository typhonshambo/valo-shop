import asyncpg
import sys
import datetime

# Set up logging
from commands.ready.logging_config import setup_logging
logger = setup_logging()

async def create_pool(dsn):
    """
    Create a connection pool to the PostgreSQL database.

    Parameters:
    - dsn (str): The data source name for connecting to the database.

    Returns:
    - pool (asyncpg.Pool): A connection pool object.
    """
    try:
        pool = await asyncpg.create_pool(dsn, max_size=4, min_size=1)
        logger.info("Database connected")
        return pool
    except Exception as e:
        logger.error(f"Failed to connect database: {e}")
        raise

async def fetch_user_data(connection, user_id):
    """
    Fetch user data from the database based on the user ID.

    Parameters:
    - connection (asyncpg.Connection): The connection to the database.
    - user_id (str): The user ID to fetch data for.

    Returns:
    - user_data (dict): User data fetched from the database, or None if not found.
    """
    try:
        query = "SELECT * FROM shopDB WHERE user_id = $1"
        user_data = await connection.fetchrow(query, user_id)
        if user_data:
            logger.info(f"Fetched user data for user ID {user_id}")
        else:
            logger.warning(f"No user data found for user ID {user_id}")
        return user_data
    except Exception as e:
        logger.error(f"Failed to fetch user data for {user_id}: {e}")
        raise

async def insert_user_data(connection, guild_id, user_id, username, password, access_token, entitlements_token, ingame_user_id, region):
    """
    Insert user data into the database.

    Parameters:
    - connection (asyncpg.Connection): The connection to the database.
    - guild_id (str): The ID of the guild.
    - user_id (str): The ID of the user.
    - username (str): The username.
    - password (str): The password.
    - access_token (str): The access token.
    - entitlements_token (str): The entitlements token.
    - ingame_user_id (str): The in-game user ID.
    - region (str): The region.

    Returns:
    - None
    """
    try:
        query = """
            INSERT INTO shopDB (guild_id, user_id, username, password, access_token, entitlements_token, ingameUserID, region)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        """
        await connection.execute(query, guild_id, user_id, username, password, access_token, entitlements_token, ingame_user_id, region)
        logger.info(f"{user_id} data inserted into the database")
    except Exception as e:
        logger.error(f"{user_id} Failed to insert user data: {e}")
        raise

async def update_user_data(connection, username, password, region, access_token, entitlements_token, ingame_user_id, user_id):
    """
    Update user data in the database.

    Parameters:
    - connection (asyncpg.Connection): The connection to the database.
    - username (str): The username.
    - password (str): The password.
    - region (str): The region.
    - access_token (str): The access token.
    - entitlements_token (str): The entitlements token.
    - ingame_user_id (str): The in-game user ID.
    - user_id (str): The ID of the user.

    Returns:
    - None
    """
    try:
        query = """
            UPDATE shopDB
            SET username = $1, password = $2, region = $3, access_token = $4, entitlements_token = $5, ingameUserID = $6
            WHERE user_id = $7
        """
        await connection.execute(query, username, password, region, access_token, entitlements_token, ingame_user_id, user_id)
        logger.info(f"{user_id} data updated in the database")
    except Exception as e:
        logger.error(f"Failed to update user data: {e}")
        raise


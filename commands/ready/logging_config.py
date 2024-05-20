import logging

def setup_logging():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(name)s: %(message)s',
        handlers=[logging.StreamHandler()]
    )

    # Get a logger for your module
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)  # Set the level for this specific logger

    # Exclude logs from discord.gateway module because it SPAMS a lot
    logging.getLogger('discord.gateway').setLevel(logging.CRITICAL)

    return logger

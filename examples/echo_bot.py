#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple echo bot using GramBotPy.
"""

import os
import sys
import logging

# Add the parent directory to the path so we can import GramBotPy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from GramBotPy import GramBotPy

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Get the bot token from environment variable
TOKEN = '7638299965:AAEOBaOwGUdq6PlmAi40WxdsQKhxp0Webks'
def main():
    """Start the bot."""
    # Create the GramBotPy instance
    bot = GramBotPy(TOKEN)
    
    # Register handlers
    @bot.on_message()
    async def echo(client, message):
        """Echo the user message."""
        # Log the message
        logger.info(f"Received message from {message.from_user.get('id')}: {message.text}")
        
        # Echo the message text back to the user
        await message.reply(message.text)
    
    # Run the bot until you press Ctrl-C
    logger.info("Starting bot...")
    bot.run()

if __name__ == '__main__':
    main() 
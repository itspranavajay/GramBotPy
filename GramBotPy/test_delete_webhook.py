import asyncio
import sys

# Add parent directory to path
sys.path.insert(0, '.')

from GramBotPy import GramBotPy

async def main():
    # Create bot instance (replace with your actual token)
    bot = GramBotPy('YOUR_BOT_TOKEN')
    
    # Check if delete_webhook method exists
    print("Bot methods:", [method for method in dir(bot) if not method.startswith('_')])
    
    # Check if delete_webhook is directly accessible
    if hasattr(bot, 'delete_webhook'):
        print("delete_webhook method is accessible")
    else:
        print("delete_webhook method is NOT accessible")

if __name__ == "__main__":
    asyncio.run(main()) 
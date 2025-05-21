import asyncio
import sys

# Add parent directory to path
sys.path.insert(0, '.')

from GramBotPy import GramBotPy

async def main():
    # Replace this with your actual bot token
    bot_token = "YOUR_BOT_TOKEN"
    
    # Create bot instance
    bot = GramBotPy(bot_token)
    
    print("Deleting webhook...")
    try:
        # Call delete_webhook with drop_pending_updates=True
        result = await bot.delete_webhook(drop_pending_updates=True)
        
        if result:
            print("Successfully deleted webhook!")
            print("You can now use getUpdates method without the 409 error.")
        else:
            print("Failed to delete webhook.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 
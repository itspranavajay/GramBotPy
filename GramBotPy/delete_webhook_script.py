import asyncio
import aiohttp
import json

async def delete_webhook(bot_token, drop_pending_updates=False):
    """Delete the webhook for a Telegram bot."""
    base_url = f"https://api.telegram.org/bot{bot_token}"
    url = f"{base_url}/deleteWebhook"
    
    params = {}
    if drop_pending_updates:
        params["drop_pending_updates"] = True
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params) as response:
            result = await response.json()
            print(f"Webhook deletion result: {result}")
            return result

async def main():
    # Replace with your actual bot token
    bot_token = "YOUR_BOT_TOKEN"  # Replace this with your actual token
    
    print("Deleting webhook...")
    result = await delete_webhook(bot_token, drop_pending_updates=True)
    
    if result.get("ok"):
        print("Successfully deleted webhook!")
        print("You can now use getUpdates method without the 409 error.")
    else:
        print(f"Failed to delete webhook: {result}")

if __name__ == "__main__":
    asyncio.run(main()) 
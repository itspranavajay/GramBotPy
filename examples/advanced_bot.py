#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
An advanced example showcasing GramBotPy's features for Telegram bots.
This example demonstrates all major functions available in GramBotPy.
"""

import os
import sys
import logging
import asyncio
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import GramBotPy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from GramBotPy import GramBotPy
from GramBotPy.types import InlineKeyboardMarkup, InlineKeyboardButton

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Get the bot token from environment variable
TOKEN = '7638299965:AAEOBaOwGUdq6PlmAi40WxdsQKhxp0Webks'

# Dictionary to store user data
user_data = {}

async def main():
    """Run the bot."""
    # Create the GramBotPy instance
    bot = GramBotPy(TOKEN)
    
    # Start the bot
    await bot.start()
    
    # Get bot information
    me = await bot.get_me()
    logger.info(f"Bot started: @{me.username}")
    
    try:
        # Register message handler for commands
        @bot.on_message()
        async def command_handler(client, message):
            """Handle commands."""
            if not message.text:
                return
                
            # Handle /start command
            if message.text == "/start":
                # Send welcome message with inline keyboard
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Help", callback_data="help"),
                     InlineKeyboardButton("About", callback_data="about")],
                    [InlineKeyboardButton("Example.com", url="https://example.com")]
                ])
                
                await message.reply(
                    f"Hello, {message.from_user.get('first_name', 'user')}!\n\n"
                    f"I'm a GramBotPy example. You can use me to test various Telegram bot features.",
                    reply_markup=keyboard
                )
                
            # Handle /help command
            elif message.text == "/help":
                await message.reply(
                    "Available commands:\n\n"
                    "/start - Start the bot\n"
                    "/help - Show this help message\n"
                    "/about - Show information about the bot\n"
                    "/keyboard - Show keyboard example\n"
                    "/photo - Send a photo\n"
                    "/admin - Show admin commands (for group admins)\n"
                    "/edit - Edit message example\n"
                    "/delete - Delete message example\n"
                    "/media - Media handling examples\n"
                    "/updates - Get updates example\n"
                    "/chat - Get chat information"
                )
                
            # Handle /about command
            elif message.text == "/about":
                await message.reply(
                    "GramBotPy Example\n\n"
                    "This is an example bot showcasing the features of the GramBotPy framework.\n\n"
                    "GramBotPy combines the features of Telethon with the organization of Pyrogram."
                )
                
            # Handle /keyboard command
            elif message.text == "/keyboard":
                # Create a more complex inline keyboard
                keyboard = InlineKeyboardMarkup()
                
                # Method 1: Add a complete row of buttons
                keyboard.row(
                    InlineKeyboardButton("Row 1, Button 1", callback_data="r1b1"),
                    InlineKeyboardButton("Row 1, Button 2", callback_data="r1b2")
                )
                
                # Method 2: Add a button as a separate row
                keyboard.add(
                    InlineKeyboardButton("Row 2, Button 1", callback_data="r2b1")
                )
                
                # Method 3: Add row from list
                keyboard.row(
                    InlineKeyboardButton("Row 3, Button 1", callback_data="r3b1"),
                    InlineKeyboardButton("Row 3, Button 2", callback_data="r3b2"),
                    InlineKeyboardButton("Row 3, Button 3", callback_data="r3b3")
                )
                
                await message.reply(
                    "This is an example of an inline keyboard:",
                    reply_markup=keyboard
                )
                
            # Handle /photo command
            elif message.text == "/photo":
                # Example of sending a photo
                await client.send_photo(
                    chat_id=message.chat_id,
                    photo="https://example.com/photo.jpg",
                    caption="This is an example photo.",
                    parse_mode="html",
                    disable_notification=False
                )
                
                # Alternative method using message.reply_photo
                await message.reply("Now sending another photo...")
                await asyncio.sleep(1)
                
                await client.send_photo(
                    chat_id=message.chat_id,
                    photo="https://example.com/another_photo.jpg",
                    caption="<b>Photo with HTML formatting</b>",
                    parse_mode="html"
                )
                
            # Handle /edit command
            elif message.text == "/edit":
                # Example of editing messages
                sent_msg = await message.reply("Original message that will be edited in 2 seconds...")
                
                # Store sent message ID for later reference
                user_data[f"edit_msg_{message.from_user.get('id')}"] = sent_msg.message_id
                
                await asyncio.sleep(2)
                
                # Edit the message text
                edited_msg = await client.edit_message_text(
                    chat_id=message.chat_id,
                    message_id=sent_msg.message_id,
                    text="This message has been edited!",
                    parse_mode="markdown"
                )
                
                await asyncio.sleep(2)
                
                # Edit again with inline keyboard
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Button added by edit", callback_data="edit_btn")]
                ])
                
                await client.edit_message_text(
                    chat_id=message.chat_id,
                    message_id=sent_msg.message_id,
                    text="This message now has an inline keyboard!",
                    reply_markup=keyboard
                )
                
            # Handle /delete command
            elif message.text == "/delete":
                # Example of deleting messages
                sent_msg = await message.reply("This message will be deleted in 3 seconds...")
                await asyncio.sleep(3)
                
                # Delete the message
                await client.delete_messages(
                    chat_id=message.chat_id,
                    message_ids=sent_msg.message_id
                )
                
                # Send confirmation
                conf_msg = await message.reply("Message deleted!")
                await asyncio.sleep(2)
                
                # Delete multiple messages at once
                await client.delete_messages(
                    chat_id=message.chat_id,
                    message_ids=[message.message_id, conf_msg.message_id]
                )
                
            # Handle /media command
            elif message.text == "/media":
                # Show media handling examples
                media_msg = await message.reply(
                    "Media Handling Examples:\n\n"
                    "1. /send_photo - Send a photo\n"
                    "2. /send_video - Send a video\n"
                    "3. /send_document - Send a document\n"
                    "4. /send_audio - Send an audio file\n"
                    "5. /download - Download media example"
                )
                
            # Handle media sub-commands
            elif message.text == "/send_photo":
                await client.send_photo(
                    chat_id=message.chat_id,
                    photo="https://enhanceaiart.s3.us-west-2.amazonaws.com/uploads/bcac916a-25aa-4ad5-9a65-f1b199f08ad9.png",
                    caption="Example photo"
                )
                
            elif message.text == "/send_video":
                await client.send_video(
                    chat_id=message.chat_id,
                    video="https://enhanceaiart.s3.us-west-2.amazonaws.com/uploads/b1180a02-4f76-4afe-9689-bf61e007da61.mp4",
                    caption="Example video",
                    duration=10,
                    width=480,
                    height=360
                )
                
            elif message.text == "/send_document":
                await client.send_document(
                    chat_id=message.chat_id,
                    document="https://example.com/document.pdf",
                    caption="Example document"
                )
                
            elif message.text == "/send_audio":
                await client.send_audio(
                    chat_id=message.chat_id,
                    audio="https://example.com/audio.mp3",
                    caption="Example audio",
                    duration=180,
                    performer="Artist",
                    title="Song Title"
                )
                
            elif message.text == "/download":
                # This is a placeholder for download example
                # In a real bot, you would download media from a message
                await message.reply("To download media, send me a photo, video, or document.")
                
                # If this was a real photo message, we would do:
                # file_path = await client.download_media(message)
                # await message.reply(f"File downloaded to: {file_path}")
                
            # Handle /updates command
            elif message.text == "/updates":
                # Example of getting updates
                await message.reply("Fetching recent updates...")
                
                # Get updates
                updates = await client.get_updates(
                    offset=0,
                    limit=5,
                    timeout=0,
                    allowed_updates=["message", "callback_query"]
                )
                
                if updates:
                    update_text = "Recent updates:\n\n"
                    for update in updates:
                        update_text += f"Update ID: {update.update_id}\n"
                        update_text += f"Type: {next((k for k, v in update.__dict__.items() if v and k != 'update_id' and k != '_client'), 'unknown')}\n\n"
                    
                    await message.reply(update_text)
                else:
                    await message.reply("No recent updates found.")
                
            # Handle /chat command
            elif message.text == "/chat":
                # Example of getting chat information
                chat = await client.get_chat(message.chat_id)
                
                chat_info = (
                    f"Chat Information:\n\n"
                    f"ID: {chat.get('id')}\n"
                    f"Type: {chat.get('type')}\n"
                    f"Title: {chat.get('title', 'N/A')}\n"
                    f"Username: {chat.get('username', 'N/A')}\n"
                )
                
                await message.reply(chat_info)
                
            # Handle /admin command
            elif message.text == "/admin":
                # Get chat and check if the user is an admin
                chat = await client.get_chat(message.chat_id)
                
                if chat.get("type") == "private":
                    await message.reply("This command only works in groups.")
                    return
                
                # In a real implementation, we would check if the user is an admin
                # For this example, we'll just show the admin commands
                admin_commands = (
                    "Admin commands:\n\n"
                    "/ban <user_id> [reason] - Ban a user\n"
                    "/unban <user_id> - Unban a user\n"
                    "/pin - Pin the replied message\n"
                    "/unpin - Unpin the pinned message\n"
                    "/promote <user_id> - Promote a user to admin\n"
                    "/demote <user_id> - Demote an admin to regular user"
                )
                
                await message.reply(admin_commands)
                
            # Handle /ban command
            elif message.text.startswith("/ban"):
                # Check if the message is in a group
                chat = await client.get_chat(message.chat_id)
                if chat.get("type") == "private":
                    await message.reply("This command only works in groups.")
                    return
                
                # Parse command arguments
                parts = message.text.split(" ", 2)
                if len(parts) < 2:
                    await message.reply("Usage: /ban <user_id> [reason]")
                    return
                
                try:
                    user_id = int(parts[1])
                    reason = parts[2] if len(parts) > 2 else "No reason provided"
                    
                    # Ban the user for 24 hours
                    ban_until = datetime.now() + timedelta(days=1)
                    success = await client.ban_chat_member(
                        chat_id=message.chat_id,
                        user_id=user_id,
                        until_date=ban_until,
                        revoke_messages=True
                    )
                    
                    if success:
                        await message.reply(f"User {user_id} banned for 24 hours.\nReason: {reason}")
                    else:
                        await message.reply("Failed to ban user.")
                        
                except ValueError:
                    await message.reply("Invalid user ID. Please provide a valid integer ID.")
                except Exception as e:
                    logger.error(f"Error banning user: {e}")
                    await message.reply(f"An error occurred: {str(e)}")
                    
            # Handle /unban command
            elif message.text.startswith("/unban"):
                # Check if the message is in a group
                chat = await client.get_chat(message.chat_id)
                if chat.get("type") == "private":
                    await message.reply("This command only works in groups.")
                    return
                
                # Parse command arguments
                parts = message.text.split(" ", 1)
                if len(parts) < 2:
                    await message.reply("Usage: /unban <user_id>")
                    return
                
                try:
                    user_id = int(parts[1])
                    
                    # Unban the user
                    success = await client.unban_chat_member(
                        chat_id=message.chat_id,
                        user_id=user_id
                    )
                    
                    if success:
                        await message.reply(f"User {user_id} has been unbanned.")
                    else:
                        await message.reply("Failed to unban user.")
                        
                except ValueError:
                    await message.reply("Invalid user ID. Please provide a valid integer ID.")
                except Exception as e:
                    logger.error(f"Error unbanning user: {e}")
                    await message.reply(f"An error occurred: {str(e)}")
                    
            # Check if message contains media for download example
            if hasattr(message, 'photo') and message.photo:
                # Example of downloading media
                await message.reply("Downloading your photo...")
                
                file_path = await client.download_media(
                    message,
                    file_name="downloads/photo.jpg",
                    progress=download_progress,
                    progress_args=(message,)
                )
                
                if file_path:
                    await message.reply(f"Photo downloaded to: {file_path}")
                else:
                    await message.reply("Failed to download photo.")
        
        # Register callback query handler
        @bot.on_callback_query()
        async def callback_handler(client, callback_query):
            """Handle callback queries from inline keyboards."""
            # Handle callback data
            if callback_query.data == "help":
                # Example of answering callback query with notification
                await callback_query.answer("Help selected", show_alert=False)
                
                # Example of editing message text from callback
                await callback_query.edit_message_text(
                    "Available commands:\n\n"
                    "/start - Start the bot\n"
                    "/help - Show this help message\n"
                    "/about - Show information about the bot\n"
                    "/keyboard - Show keyboard example\n"
                    "/photo - Send a photo\n"
                    "/admin - Show admin commands (for group admins)\n"
                    "/edit - Edit message example\n"
                    "/delete - Delete message example\n"
                    "/media - Media handling examples\n"
                    "/updates - Get updates example\n"
                    "/chat - Get chat information"
                )
                
            elif callback_query.data == "about":
                # Example of answering callback query with alert
                await callback_query.answer("About selected", show_alert=True)
                
                await callback_query.edit_message_text(
                    "GramBotPy Example\n\n"
                    "This is an example bot showcasing the features of the GramBotPy framework.\n\n"
                    "GramBotPy combines the features of Telethon with the organization of Pyrogram."
                )
                
            elif callback_query.data == "edit_btn":
                # Example of handling button added by edit
                await callback_query.answer("You clicked the button added by edit")
                await callback_query.edit_message_text("Button clicked! This message was edited again.")
                
            elif callback_query.data.startswith("r"):
                # Display which button was pressed with different answer types
                row, button = callback_query.data[1], callback_query.data[3]
                
                if row == "1":
                    # Simple notification
                    await callback_query.answer(f"You pressed button {button} in row {row}")
                elif row == "2":
                    # Alert dialog
                    await callback_query.answer(
                        f"This is an alert dialog.\nYou pressed button {button} in row {row}",
                        show_alert=True
                    )
                elif row == "3":
                    # Edit message with new keyboard
                    await callback_query.answer()  # Silent answer
                    
                    # Create a "back" button keyboard
                    back_keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("⬅️ Back", callback_data="back")]
                    ])
                    
                    await callback_query.edit_message_text(
                        f"You selected: Row {row}, Button {button}",
                        reply_markup=back_keyboard
                    )
                    
            elif callback_query.data == "back":
                # Handle back button by recreating original keyboard
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Row 1, Button 1", callback_data="r1b1"),
                     InlineKeyboardButton("Row 1, Button 2", callback_data="r1b2")],
                    [InlineKeyboardButton("Row 2, Button 1", callback_data="r2b1")],
                    [InlineKeyboardButton("Row 3, Button 1", callback_data="r3b1"),
                     InlineKeyboardButton("Row 3, Button 2", callback_data="r3b2"),
                     InlineKeyboardButton("Row 3, Button 3", callback_data="r3b3")]
                ])
                
                await callback_query.answer()
                await callback_query.edit_message_text(
                    "This is an example of an inline keyboard:",
                    reply_markup=keyboard
                )
                
            else:
                await callback_query.answer("Unknown callback query")
                
        # Define a progress callback for downloads
        async def download_progress(current, total, file_name, args):
            """Show download progress."""
            message = args[0]
            percent = current * 100 // total
            
            # Update progress every 10%
            if current == total or percent % 10 == 0:
                await client.send_message(
                    chat_id=message.chat_id,
                    text=f"Download progress: {percent}%"
                )
        
        # Keep the bot running until interrupted
        logger.info("Bot is running. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        # Stop the bot on Ctrl+C
        logger.info("Bot stopped by user.")
    finally:
        # Disconnect the bot
        await bot.stop()

if __name__ == '__main__':
    asyncio.run(main()) 
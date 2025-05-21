import asyncio
import os
import sys
import json
from datetime import datetime, timedelta

# Add parent directory to path so Python can find the GramBotPy module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from GramBotPy import *
from GramBotPy.types import *

"""
Complete Example of GramBotPy Features

This example demonstrates ALL features of GramBotPy including:
1. Basic bot commands
2. Inline keyboards and callbacks
3. Database operations
4. Message handling
5. File operations (photos, audio, video, documents)
6. User management
7. Channel and group management
8. Inline queries
9. Location sharing
10. Contact sharing
11. Stickers and animations
12. Message editing and deletion
13. Deep linking
14. Games
15. Polls and quizzes
16. Error handling
"""

async def main():
    # Initialize bot with your token
    bot = GramBotPy("7361511720:AAHqI8PNFoi0NItdufzgilVaeN5rhVJDdQo")
    
    # Delete any existing webhook before using getUpdates method
    print("Deleting webhook...")
    result = await bot.delete_webhook(drop_pending_updates=True)
    if result:
        print("Successfully deleted webhook!")
        print("Now the bot can use getUpdates method without the 409 error.")
    else:
        print("Failed to delete webhook.")
    
    await bot.start()
    
    print("=== GRAMBOTPY COMPLETE EXAMPLE ===")
    
    # ===== BASIC COMMANDS =====
    @bot.command("start")
    async def start_command(message: Message):
        """Handle /start command"""
        # Check for deep linking parameters
        args = message.text.split()
        if len(args) > 1:
            deep_link_param = args[1]
            await message.reply(
                f"Welcome to GramBotPy! 🚀\n"
                f"You came here with parameter: {deep_link_param}\n"
                f"Use /help to see available commands."
            )
        else:
            await message.reply(
                "Welcome to GramBotPy! 🚀\n"
                "Use /help to see available commands."
            )
    
    @bot.command("help")
    async def help_command(message: Message):
        """Handle /help command"""
        help_text = """
Available Commands:
/start - Start the bot
/help - Show this help message
/echo [text] - Echo your message
/button - Show inline buttons
/db - Database operations
/file - File operations
/sendphoto - Photo examples
/sendaudio - Audio examples
/sendvideo - Video examples
/sendlocation - Location examples
/sendcontact - Contact examples
/sendsticker - Sticker examples
/message - Message operations
/group - Group management
/inline - Inline query info
/game - Game example
/poll - Poll example
/quiz - Quiz example
/userinfo - User information
/channel - Channel operations
"""
        await message.reply(help_text)
    
    @bot.command("echo")
    async def echo_command(message: Message):
        """Handle /echo command"""
        if len(message.text.split()) > 1:
            text = " ".join(message.text.split()[1:])
            await message.reply(f"Echo: {text}")
        else:
            await message.reply("Please provide text to echo!")
    
    # ===== INLINE KEYBOARD EXAMPLE =====
    @bot.command("button")
    async def button_command(message: Message):
        """Show inline keyboard buttons"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Option 1", callback_data="opt1"),
                InlineKeyboardButton("Option 2", callback_data="opt2")
            ],
            [
                InlineKeyboardButton("Visit Website", url="https://example.com")
            ],
            [
                InlineKeyboardButton("Show Alert", callback_data="alert")
            ]
        ])
        
        await message.reply(
            "Choose an option:",
            reply_markup=keyboard
        )
    
    @bot.callback_query("opt1")
    async def option1_callback(callback: CallbackQuery):
        """Handle Option 1 callback"""
        await callback.answer("You selected Option 1!")
        await callback.message.edit_text("You selected Option 1!")
    
    @bot.callback_query("opt2")
    async def option2_callback(callback: CallbackQuery):
        """Handle Option 2 callback"""
        await callback.answer("You selected Option 2!")
        await callback.message.edit_text("You selected Option 2!")
    
    @bot.callback_query("alert")
    async def alert_callback(callback: CallbackQuery):
        """Handle alert callback"""
        await callback.answer("This is an alert message!", show_alert=True)
    
    # ===== DATABASE OPERATIONS =====
    @bot.command("db")
    async def db_command(message: Message):
        """Demonstrate database operations"""
        # Create database and collection
        db = bot.get_database("example_db")
        users = db.collection("users", "@your_channel_id")
        products = db.collection("products", "@your_products_channel")
        
        # Insert user data
        user_data = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "joined_date": datetime.now().isoformat()
        }
        
        # Insert document
        result = await users.insert_one(user_data)
        
        # Find user
        user = await users.find_one({"user_id": message.from_user.id})
        
        # Insert product data
        product_data = {
            "name": "Sample Product",
            "price": 99.99,
            "category": "Electronics",
            "in_stock": True,
            "tags": ["sample", "electronics", "new"],
            "created_at": datetime.now().isoformat()
        }
        
        # Insert product
        product_result = await products.insert_one(product_data)
        
        # Find products
        all_products = await products.find({"in_stock": True})
        
        # Update a product
        await products.update_one(
            {"name": "Sample Product"},
            {"price": 89.99, "in_stock": False}
        )
        
        # Count documents
        product_count = await products.count_documents()
        
        # Delete a document
        await products.delete_one({"name": "Sample Product"})
        
        if user:
            await message.reply(
                f"Database operations successful!\n"
                f"User ID: {user.data['user_id']}\n"
                f"Username: {user.data['username']}\n"
                f"Joined: {user.data['joined_date']}\n\n"
                f"Product count: {product_count}\n"
                f"Product deleted: {product_data['name']}"
            )
    
    # ===== FILE OPERATIONS =====
    @bot.command("file")
    async def file_command(message: Message):
        """Demonstrate file operations"""
        # Send a file
        await message.reply_document(
            document="path/to/your/file.txt",
            caption="Here's a file!"
        )
        
        # Send a photo
        await message.reply_photo(
            photo="path/to/your/photo.jpg",
            caption="Here's a photo!"
        )
        
        # Send multiple photos as album
        await message.reply_media_group([
            {
                "type": "photo",
                "media": "path/to/photo1.jpg",
                "caption": "Photo 1"
            },
            {
                "type": "photo",
                "media": "path/to/photo2.jpg",
                "caption": "Photo 2"
            }
        ])
        
        # Send audio file
        await message.reply_audio(
            audio="path/to/your/audio.mp3",
            title="Song Title",
            performer="Artist Name",
            duration=180,  # Duration in seconds
            caption="Here's an audio file!"
        )
        
        # Send voice message
        await message.reply_voice(
            voice="path/to/your/voice.ogg",
            duration=30,  # Duration in seconds
            caption="Here's a voice message!"
        )
        
        # Download file example
        if message.document:
            file_info = await bot.get_file(message.document.file_id)
            downloaded_file = await bot.download_file(file_info.file_path)
            
            # Save to disk
            with open("downloaded_file.txt", "wb") as f:
                f.write(downloaded_file)
            
            await message.reply("File downloaded successfully!")

    @bot.command("sendphoto")
    async def send_photo_command(message: Message):
        """Send photo with different options"""
        # Send photo with caption
        await message.reply_photo(
            photo="https://enhanceaiart.s3.us-west-2.amazonaws.com/uploads/bcac916a-25aa-4ad5-9a65-f1b199f08ad9.png",
            caption="Beautiful sunset! 🌅",
            parse_mode="HTML"
        )
        
        # Send photo with custom keyboard
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Like 👍", callback_data="like_photo")],
            [InlineKeyboardButton("Share 🔗", callback_data="share_photo")]
        ])
        
        await message.reply_photo(
            photo="path/to/photo.jpg",
            caption="Photo with interactive buttons!",
            reply_markup=keyboard
        )
        
        # Send photo by URL
        await message.reply_photo(
            photo="https://example.com/photo.jpg",
            caption="Photo from URL"
        )
        
        # Send photo by file_id (if available)
        if message.photo:
            file_id = message.photo[-1].file_id  # Get largest photo file_id
            await message.reply_photo(
                photo=file_id,
                caption="Photo sent using file_id"
            )

    @bot.command("sendaudio")
    async def send_audio_command(message: Message):
        """Send audio with different options"""
        # Send audio file with metadata
        await message.reply_audio(
            audio="path/to/song.mp3",
            title="Amazing Song",
            performer="Famous Artist",
            duration=240,  # 4 minutes
            caption="🎵 Listen to this amazing track!",
            thumb="path/to/thumbnail.jpg"  # Optional thumbnail
        )
        
        # Send voice message
        await message.reply_voice(
            voice="path/to/voice.ogg",
            duration=45,  # 45 seconds
            caption="🎤 Voice message"
        )
        
        # Send audio with custom keyboard
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Download ⬇️", callback_data="download_audio")],
            [InlineKeyboardButton("Play ▶️", callback_data="play_audio")]
        ])
        
        await message.reply_audio(
            audio="path/to/audio.mp3",
            title="Interactive Audio",
            performer="Artist",
            duration=180,
            caption="Audio with interactive buttons!",
            reply_markup=keyboard
        )
        
        # Send audio by file_id (if available)
        if message.audio:
            file_id = message.audio.file_id
            await message.reply_audio(
                audio=file_id,
                caption="Audio sent using file_id"
            )

    @bot.command("sendvideo")
    async def send_video_command(message: Message):
        """Send video with different options"""
        # Send video file
        await message.reply_video(
            video="path/to/video.mp4",
            caption="Check out this video!",
            width=1280,
            height=720,
            duration=60,  # 1 minute
            supports_streaming=True
        )
        
        # Send video note (round message)
        await message.reply_video_note(
            video_note="path/to/video_note.mp4",
            duration=15,
            length=240  # Video note dimension (it's a square)
        )
        
        # Send mixed media group (photos and videos)
        await message.reply_media_group([
            {
                "type": "photo",
                "media": "path/to/photo.jpg",
                "caption": "Mixed media album"
            },
            {
                "type": "video",
                "media": "path/to/video.mp4",
                "caption": "Video in album"
            }
        ])
        
        # Send animation (GIF)
        await message.reply_animation(
            animation="path/to/animation.gif",
            caption="Funny GIF",
            width=480,
            height=320,
            duration=5
        )

    @bot.command("sendlocation")
    async def send_location_command(message: Message):
        """Send location with different options"""
        # Send static location
        await message.reply_location(
            latitude=40.7128,
            longitude=-74.0060,
            horizontal_accuracy=50  # Accuracy radius in meters
        )
        
        # Send live location (updates for a period)
        await message.reply_location(
            latitude=40.7128,
            longitude=-74.0060,
            live_period=60 * 15  # Live for 15 minutes
        )
        
        # Send venue (location with additional details)
        await message.reply_venue(
            latitude=40.7128,
            longitude=-74.0060,
            title="New York City",
            address="Manhattan, NY, USA",
            foursquare_id="OPTIONAL_FOURSQUARE_ID"
        )

    @bot.command("sendcontact")
    async def send_contact_command(message: Message):
        """Send contact information"""
        # Send a contact
        await message.reply_contact(
            phone_number="+1234567890",
            first_name="John",
            last_name="Doe",
            vcard="OPTIONAL_VCARD_DATA"
        )
        
        # Send multiple contacts with keyboard
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Call Contact", callback_data="call_contact")]
        ])
        
        await message.reply_contact(
            phone_number="+9876543210",
            first_name="Jane",
            last_name="Smith",
            reply_markup=keyboard
        )

    @bot.command("sendsticker")
    async def send_sticker_command(message: Message):
        """Send stickers and sticker sets"""
        # Send a sticker
        await message.reply_sticker(
            sticker="path/to/sticker.webp"
        )
        
        # Send animated sticker
        await message.reply_sticker(
            sticker="path/to/animated_sticker.tgs"
        )
        
        # Send sticker by file_id (if available)
        if message.sticker:
            sticker_id = message.sticker.file_id
            await message.reply_sticker(
                sticker=sticker_id
            )
        
        # Get sticker set information
        if message.sticker and message.sticker.set_name:
            sticker_set = await bot.get_sticker_set(message.sticker.set_name)
            await message.reply(f"Sticker set: {sticker_set.title}")

    # ===== MESSAGE OPERATIONS =====
    @bot.command("message")
    async def message_operations_command(message: Message):
        """Demonstrate message operations"""
        # Send message with formatting
        formatted_message = await message.reply(
            "This message has *bold* and _italic_ formatting, as well as [links](https://example.com).",
            parse_mode="Markdown"
        )
        
        # Edit message
        await asyncio.sleep(2)
        await formatted_message.edit_text(
            "This message has been *edited*!",
            parse_mode="Markdown"
        )
        
        # Send HTML formatted message
        html_message = await message.reply(
            "<b>HTML</b> formatting with <i>styles</i> and <a href='https://example.com'>links</a>.",
            parse_mode="HTML"
        )
        
        # Add reaction to message
        await message.react("👍")
        
        # Pin message
        await html_message.pin()
        await message.reply("Message pinned!")
        
        # Forward message
        if message.reply_to_message:
            forwarded = await message.reply_to_message.forward(message.chat.id)
            await message.reply("Message forwarded!")
        
        # Delete message after delay
        temp_message = await message.reply("This message will be deleted in 5 seconds...")
        await asyncio.sleep(5)
        await temp_message.delete()
    
    # ===== GROUP MANAGEMENT =====
    @bot.command("group")
    async def group_management_command(message: Message):
        """Demonstrate group management operations"""
        if not message.chat.type in ["group", "supergroup"]:
            await message.reply("This command is for groups only!")
            return
        
        # Get chat info
        chat = await bot.get_chat(message.chat.id)
        
        # Get chat member count
        member_count = await bot.get_chat_member_count(message.chat.id)
        
        # Get chat administrators
        admins = await bot.get_chat_administrators(message.chat.id)
        admin_usernames = [f"@{admin.user.username}" for admin in admins if admin.user.username]
        
        # Get bot's permissions
        bot_member = await bot.get_chat_member(message.chat.id, (await bot.get_me()).id)
        
        # Ban a user (example only - will not actually ban anyone)
        # await bot.ban_chat_member(message.chat.id, user_id_to_ban)
        
        # Kick a user (example only - will not actually kick anyone)
        # await bot.ban_chat_member(message.chat.id, user_id_to_kick, until_date=datetime.now() + timedelta(seconds=5))
        
        # Restrict a user (example only - will not actually restrict anyone)
        # await bot.restrict_chat_member(
        #     message.chat.id, 
        #     user_id_to_restrict,
        #     permissions={
        #         "can_send_messages": False,
        #         "can_send_media_messages": False,
        #     },
        #     until_date=datetime.now() + timedelta(minutes=60)
        # )
        
        # Set chat title (if bot is admin)
        # await bot.set_chat_title(message.chat.id, "New Group Title")
        
        # Set chat description (if bot is admin)
        # await bot.set_chat_description(message.chat.id, "New group description")
        
        # Set chat photo (if bot is admin)
        # await bot.set_chat_photo(message.chat.id, "path/to/new_photo.jpg")
        
        await message.reply(
            f"Group information:\n"
            f"Title: {chat.title}\n"
            f"Type: {chat.type}\n"
            f"Description: {chat.description or 'None'}\n"
            f"Member count: {member_count}\n"
            f"Administrators: {', '.join(admin_usernames) if admin_usernames else 'None'}\n"
        )
    
    # Handle new chat members
    @bot.message_handler("new_chat_members")
    async def welcome_new_members(message: Message):
        """Welcome new chat members"""
        if hasattr(message, 'new_chat_members') and message.new_chat_members:
            for new_member in message.new_chat_members:
                if new_member.get('id') == (await bot.get_me()).id:
                    # Bot was added to a group
                    await message.reply("Thanks for adding me to this group!")
                else:
                    # New user joined
                    first_name = new_member.get('first_name', 'User')
                    await message.reply(f"Welcome to the group, {first_name}!")
    
    # Handle chat join requests (for restricted groups)
    @bot.chat_join_request_handler()
    async def handle_join_request(request: ChatJoinRequest):
        """Handle chat join request"""
        # Approve or decline join request
        # await bot.approve_chat_join_request(request.chat.id, request.user.id)
        # OR
        # await bot.decline_chat_join_request(request.chat.id, request.user.id)
        pass

    # ===== INLINE QUERIES =====
    @bot.command("inline")
    async def inline_query_info(message: Message):
        """Explain inline query functionality"""
        await message.reply(
            "You can use me in inline mode by typing:\n"
            "@YourBotUsername query\n\n"
            "Try it to see the inline results!"
        )
    
    @bot.inline_query_handler()
    async def handle_inline_query(inline_query: InlineQuery):
        """Handle inline queries"""
        query = inline_query.query
        
        if not query:
            # Default results when no query
            results = [
                {
                    "type": "article",
                    "id": "default1",
                    "title": "Send a greeting",
                    "description": "Sends 'Hello from GramBotPy!'",
                    "input_message_content": {
                        "message_text": "Hello from GramBotPy! 👋"
                    }
                },
                {
                    "type": "article",
                    "id": "default2",
                    "title": "Send the current time",
                    "description": "Sends the current time",
                    "input_message_content": {
                        "message_text": f"Current time: {datetime.now().strftime('%H:%M:%S')}"
                    }
                }
            ]
        else:
            # Results based on query
            results = [
                {
                    "type": "article",
                    "id": "query1",
                    "title": f"Send: {query}",
                    "description": f"Sends your query: {query}",
                    "input_message_content": {
                        "message_text": f"You said: {query}"
                    }
                },
                {
                    "type": "article",
                    "id": "query2",
                    "title": f"Send in bold: {query}",
                    "description": "Sends your query in bold format",
                    "input_message_content": {
                        "message_text": f"*{query}*",
                        "parse_mode": "Markdown"
                    }
                }
            ]
        
        await bot.answer_inline_query(inline_query.id, results)
    
    @bot.chosen_inline_result_handler()
    async def handle_chosen_inline_result(chosen_result: ChosenInlineResult):
        """Handle when a user selects an inline result"""
        # This is triggered when a user selects one of your inline results
        # You can use this to track which results are popular
        print(f"User selected result with ID: {chosen_result.result_id}")

    # ===== GAMES =====
    @bot.command("game")
    async def game_command(message: Message):
        """Send a game"""
        # Note: You need to create a game with @BotFather first
        await message.reply_game("your_game_short_name")
        
        # Game with keyboard
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Play Now", callback_game=True)]
        ])
        
        await message.reply_game(
            "your_game_short_name",
            reply_markup=keyboard
        )
    
    @bot.callback_query_handler()
    async def general_callback_handler(callback: CallbackQuery):
        """Handle callback queries not handled by specific handlers"""
        # Handle game callback
        if callback.game_short_name:
            # Set the game URL
            await bot.answer_callback_query(
                callback.id,
                url="https://your-game-url.com"
            )

    # ===== POLLS AND QUIZZES =====
    @bot.command("poll")
    async def poll_command(message: Message):
        """Create a poll"""
        await message.reply_poll(
            question="What's your favorite programming language?",
            options=["Python", "JavaScript", "Java", "C++", "Other"],
            is_anonymous=False,
            allows_multiple_answers=True
        )
    
    @bot.command("quiz")
    async def quiz_command(message: Message):
        """Create a quiz"""
        await message.reply_poll(
            question="What is the capital of France?",
            options=["London", "Berlin", "Paris", "Madrid"],
            type="quiz",
            correct_option_id=2,
            explanation="Paris is the capital of France!"
        )
    
    # ===== USER MANAGEMENT =====
    @bot.command("userinfo")
    async def userinfo_command(message: Message):
        """Show user information"""
        user = message.from_user
        info = f"""
User Information:
ID: {user.id}
Username: @{user.username or "None"}
First Name: {user.first_name}
Last Name: {user.last_name or "None"}
Language Code: {user.language_code or "None"}
Is Bot: {user.is_bot}
"""
        await message.reply(info)
        
        # Get user profile photos
        photos = await bot.get_user_profile_photos(user.id, limit=1)
        if photos and photos.total_count > 0:
            photo = photos.photos[0][-1]  # Get the largest size of the most recent photo
            await message.reply_photo(
                photo=photo.file_id,
                caption="Your profile photo"
            )
    
    # ===== CHANNEL MANAGEMENT =====
    @bot.command("channel")
    async def channel_command(message: Message):
        """Demonstrate channel operations"""
        # Send message to channel
        await bot.send_message(
            chat_id="@your_channel",
            text="Hello from GramBotPy!"
        )
        
        # Get channel info
        channel = await bot.get_chat("@your_channel")
        
        # Get channel member count
        # member_count = await bot.get_chat_member_count("@your_channel")
        
        # Pin a message in the channel
        channel_message = await bot.send_message(
            chat_id="@your_channel",
            text="Important announcement!"
        )
        await bot.pin_chat_message(
            chat_id="@your_channel",
            message_id=channel_message.message_id,
            disable_notification=False
        )
        
        await message.reply(f"Channel Title: {channel.title}")
    
    # ===== ERROR HANDLING =====
    @bot.error_handler()
    async def error_handler(error):
        """Handle errors"""
        print(f"Error occurred: {error}")
    
    # Keep the bot running
    print("Bot is running...")
    await bot.idle()

if __name__ == "__main__":
    asyncio.run(main()) 
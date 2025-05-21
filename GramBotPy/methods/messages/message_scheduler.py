import typing
import asyncio
import uuid
import time
from datetime import datetime, timedelta
from typing import Union, Optional, Dict, Any, List, Callable, Awaitable

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class MessageScheduler:
    """Method for scheduling messages to be sent at a later time."""
    
    def __init__(self):
        """Initialize the message scheduler."""
        self._scheduled_tasks = {}
        self._running = False
        self._scheduler_task = None
    
    async def schedule_message(
        self: "GramBotPy",
        chat_id: Union[int, str],
        text: str,
        when: Union[datetime, timedelta, int, float],
        parse_mode: Optional[str] = None,
        entities: Optional[List[Dict[str, Any]]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
        task_id: Optional[str] = None
    ) -> str:
        """Schedule a text message to be sent at a specific time.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            text (``str``):
                Text of the message to be sent.
                
            when (``datetime`` | ``timedelta`` | ``int`` | ``float``):
                When to send the message. Can be:
                - A datetime object for a specific time
                - A timedelta for a delay from now
                - Seconds from now as int or float
                
            parse_mode (``str``, optional):
                Mode for parsing entities.
                
            entities (``list``, optional):
                List of special entities that appear in the message text.
                
            disable_web_page_preview (``bool``, optional):
                Disables link previews for links in this message.
                
            disable_notification (``bool``, optional):
                Sends the message silently.
                
            protect_content (``bool``, optional):
                Protects the contents of the sent message from forwarding and saving.
                
            reply_to_message_id (``int``, optional):
                If the message is a reply, ID of the original message.
                
            allow_sending_without_reply (``bool``, optional):
                Pass True if the message should be sent even if the specified replied-to
                message is not found.
                
            reply_markup (``dict``, optional):
                Additional interface options.
                
            task_id (``str``, optional):
                Custom task identifier. If not provided, a UUID will be generated.
                
        Returns:
            ``str``: Task identifier that can be used to cancel the scheduled message.
            
        Example:
            .. code-block:: python
            
                # Schedule a message to be sent after 1 hour
                from datetime import timedelta
                task_id = await bot.schedule_message(
                    chat_id, 
                    "This is a scheduled message",
                    when=timedelta(hours=1)
                )
                
                # Schedule a message for a specific time
                from datetime import datetime
                scheduled_time = datetime(2023, 12, 31, 23, 59, 59)
                task_id = await bot.schedule_message(
                    chat_id,
                    "Happy New Year!",
                    when=scheduled_time
                )
                
                # Cancel a scheduled message
                await bot.cancel_scheduled_message(task_id)
        """
        self.logger.info(f"Scheduling message to {chat_id}")
        
        # Generate task_id if not provided
        if task_id is None:
            task_id = str(uuid.uuid4())
            
        # Convert 'when' to an absolute datetime
        target_time = self._normalize_time(when)
        
        # Create the message parameters
        message_params = {
            "chat_id": chat_id,
            "text": text
        }
        
        # Add optional parameters if provided
        if parse_mode:
            message_params["parse_mode"] = parse_mode
            
        if entities:
            message_params["entities"] = entities
            
        if disable_web_page_preview is not None:
            message_params["disable_web_page_preview"] = disable_web_page_preview
            
        if disable_notification is not None:
            message_params["disable_notification"] = disable_notification
            
        if protect_content is not None:
            message_params["protect_content"] = protect_content
            
        if reply_to_message_id:
            message_params["reply_to_message_id"] = reply_to_message_id
            
        if allow_sending_without_reply is not None:
            message_params["allow_sending_without_reply"] = allow_sending_without_reply
            
        if reply_markup:
            message_params["reply_markup"] = reply_markup
            
        # Store the scheduled task
        self._scheduled_tasks[task_id] = {
            "target_time": target_time,
            "message_params": message_params,
            "method": "send_message",
            "created_at": datetime.now(),
            "status": "scheduled"
        }
        
        # Start the scheduler if not already running
        await self._ensure_scheduler_running()
        
        return task_id
    
    async def schedule_media_message(
        self: "GramBotPy",
        method: str,
        chat_id: Union[int, str],
        media: Union[str, Dict[str, Any]],
        when: Union[datetime, timedelta, int, float],
        caption: Optional[str] = None,
        task_id: Optional[str] = None,
        **kwargs
    ) -> str:
        """Schedule a media message to be sent at a specific time.
        
        Parameters:
            method (``str``):
                The method to use for sending. Must be one of:
                - 'send_photo'
                - 'send_video'
                - 'send_audio'
                - 'send_document'
                - 'send_animation'
                - 'send_voice'
                - 'send_sticker'
                
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            media (``str`` | ``dict``):
                Media to send.
                
            when (``datetime`` | ``timedelta`` | ``int`` | ``float``):
                When to send the message.
                
            caption (``str``, optional):
                Media caption.
                
            task_id (``str``, optional):
                Custom task identifier.
                
            **kwargs:
                Additional parameters specific to the method.
                
        Returns:
            ``str``: Task identifier that can be used to cancel the scheduled message.
            
        Example:
            .. code-block:: python
            
                # Schedule a photo to be sent after 30 minutes
                from datetime import timedelta
                task_id = await bot.schedule_media_message(
                    method="send_photo",
                    chat_id=chat_id,
                    media="https://example.com/image.jpg",
                    when=timedelta(minutes=30),
                    caption="Scheduled photo"
                )
        """
        self.logger.info(f"Scheduling {method} to {chat_id}")
        
        # Generate task_id if not provided
        if task_id is None:
            task_id = str(uuid.uuid4())
            
        # Convert 'when' to an absolute datetime
        target_time = self._normalize_time(when)
        
        # Create the media parameters
        media_params = {
            "chat_id": chat_id
        }
        
        # Add the appropriate media parameter name based on the method
        if method == "send_photo":
            media_params["photo"] = media
        elif method == "send_video":
            media_params["video"] = media
        elif method == "send_audio":
            media_params["audio"] = media
        elif method == "send_document":
            media_params["document"] = media
        elif method == "send_animation":
            media_params["animation"] = media
        elif method == "send_voice":
            media_params["voice"] = media
        elif method == "send_sticker":
            media_params["sticker"] = media
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        # Add caption if provided
        if caption:
            media_params["caption"] = caption
            
        # Add any additional parameters
        media_params.update(kwargs)
        
        # Store the scheduled task
        self._scheduled_tasks[task_id] = {
            "target_time": target_time,
            "message_params": media_params,
            "method": method,
            "created_at": datetime.now(),
            "status": "scheduled"
        }
        
        # Start the scheduler if not already running
        await self._ensure_scheduler_running()
        
        return task_id
    
    async def cancel_scheduled_message(
        self: "GramBotPy",
        task_id: str
    ) -> bool:
        """Cancel a scheduled message.
        
        Parameters:
            task_id (``str``):
                The task identifier returned by schedule_message.
                
        Returns:
            ``bool``: True if the message was cancelled, False otherwise.
        """
        if task_id in self._scheduled_tasks:
            self._scheduled_tasks[task_id]["status"] = "cancelled"
            self.logger.info(f"Cancelled scheduled message with task_id: {task_id}")
            return True
        
        self.logger.warning(f"Task with ID {task_id} not found.")
        return False
    
    async def get_scheduled_messages(
        self: "GramBotPy",
        chat_id: Optional[Union[int, str]] = None
    ) -> List[Dict[str, Any]]:
        """Get information about scheduled messages.
        
        Parameters:
            chat_id (``int`` | ``str``, optional):
                If provided, only return messages for this chat.
                
        Returns:
            ``list``: List of scheduled message information.
        """
        result = []
        
        for task_id, task in self._scheduled_tasks.items():
            if task["status"] != "cancelled":
                if chat_id is None or task["message_params"].get("chat_id") == chat_id:
                    result.append({
                        "task_id": task_id,
                        "chat_id": task["message_params"].get("chat_id"),
                        "method": task["method"],
                        "target_time": task["target_time"],
                        "created_at": task["created_at"],
                        "status": task["status"],
                        # Include subset of parameters for information
                        "text": task["message_params"].get("text", ""),
                        "caption": task["message_params"].get("caption", "")
                    })
                    
        return result
    
    def _normalize_time(
        self,
        when: Union[datetime, timedelta, int, float]
    ) -> datetime:
        """Convert various time formats to an absolute datetime.
        
        Parameters:
            when (``datetime`` | ``timedelta`` | ``int`` | ``float``):
                Time specification.
                
        Returns:
            ``datetime``: Absolute target time.
        """
        now = datetime.now()
        
        if isinstance(when, datetime):
            return when
        elif isinstance(when, timedelta):
            return now + when
        elif isinstance(when, (int, float)):
            return now + timedelta(seconds=when)
        else:
            raise ValueError(f"Unsupported time format: {type(when)}")
    
    async def _ensure_scheduler_running(self):
        """Ensure the scheduler is running."""
        if not self._running:
            self._running = True
            self._scheduler_task = asyncio.create_task(self._scheduler_loop())
    
    async def _scheduler_loop(self):
        """Main scheduler loop."""
        try:
            while True:
                now = datetime.now()
                
                # Find tasks that need to be executed
                for task_id, task in list(self._scheduled_tasks.items()):
                    if task["status"] == "scheduled" and task["target_time"] <= now:
                        # Mark as executing
                        task["status"] = "executing"
                        
                        # Execute the task
                        method_name = task["method"]
                        if hasattr(self, method_name):
                            method = getattr(self, method_name)
                            try:
                                await method(**task["message_params"])
                                task["status"] = "completed"
                                self.logger.info(f"Successfully executed scheduled task {task_id}")
                            except Exception as e:
                                task["status"] = "failed"
                                task["error"] = str(e)
                                self.logger.error(f"Error executing scheduled task {task_id}: {e}", exc_info=True)
                        else:
                            task["status"] = "failed"
                            task["error"] = f"Method {method_name} not found"
                            self.logger.error(f"Method {method_name} not found for task {task_id}")
                
                # Clean up old tasks (completed or cancelled older than 1 hour)
                self._clean_old_tasks()
                
                # Sleep for a bit
                await asyncio.sleep(1)
                
        except asyncio.CancelledError:
            self.logger.info("Scheduler loop cancelled.")
            self._running = False
        except Exception as e:
            self.logger.error(f"Error in scheduler loop: {e}", exc_info=True)
            self._running = False
    
    def _clean_old_tasks(self, max_age: int = 3600):
        """Clean up old completed or cancelled tasks.
        
        Parameters:
            max_age (``int``, optional):
                Maximum age in seconds. Defaults to 3600 (1 hour).
        """
        now = datetime.now()
        for task_id, task in list(self._scheduled_tasks.items()):
            if task["status"] in ["completed", "cancelled", "failed"]:
                created_at = task["created_at"]
                if (now - created_at).total_seconds() > max_age:
                    del self._scheduled_tasks[task_id]
    
    async def shutdown(self):
        """Shutdown the scheduler."""
        if self._scheduler_task:
            self._scheduler_task.cancel()
            try:
                await self._scheduler_task
            except asyncio.CancelledError:
                pass
            self._running = False 
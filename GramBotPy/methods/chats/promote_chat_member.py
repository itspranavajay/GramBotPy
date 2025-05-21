import typing
import aiohttp
import json
from typing import Union, Optional

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class PromoteChatMember:
    """Method to promote a user in a chat."""
    
    async def promote_chat_member(
        self: "GramBotPy",
        chat_id: Union[int, str],
        user_id: int,
        is_anonymous: Optional[bool] = None,
        can_manage_chat: Optional[bool] = None,
        can_post_messages: Optional[bool] = None,
        can_edit_messages: Optional[bool] = None,
        can_delete_messages: Optional[bool] = None,
        can_restrict_members: Optional[bool] = None,
        can_promote_members: Optional[bool] = None,
        can_change_info: Optional[bool] = None,
        can_invite_users: Optional[bool] = None,
        can_pin_messages: Optional[bool] = None,
        can_manage_voice_chats: Optional[bool] = None
    ) -> bool:
        """Promote or demote a user in a supergroup or a channel.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            user_id (``int``):
                Unique identifier of the target user.
                
            is_anonymous (``bool``, optional):
                Pass True, if the administrator's presence in the chat is hidden.
                
            can_manage_chat (``bool``, optional):
                Pass True, if the administrator can access the chat event log, boost list in channels, 
                see channel members, etc.
                
            can_post_messages (``bool``, optional):
                Pass True, if the administrator can create channel posts, channels only.
                
            can_edit_messages (``bool``, optional):
                Pass True, if the administrator can edit messages of other users 
                and can pin messages, channels only.
                
            can_delete_messages (``bool``, optional):
                Pass True, if the administrator can delete messages of other users.
                
            can_restrict_members (``bool``, optional):
                Pass True, if the administrator can restrict, ban or unban chat members.
                
            can_promote_members (``bool``, optional):
                Pass True, if the administrator can add new administrators with a subset 
                of their own privileges or demote administrators.
                
            can_change_info (``bool``, optional):
                Pass True, if the administrator can change chat title, photo and other settings.
                
            can_invite_users (``bool``, optional):
                Pass True, if the administrator can invite new users to the chat.
                
            can_pin_messages (``bool``, optional):
                Pass True, if the administrator can pin messages, supergroups only.
                
            can_manage_voice_chats (``bool``, optional):
                Pass True, if the administrator can manage voice chats.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Make a user admin with basic permissions
                await bot.promote_chat_member(
                    chat_id, user_id,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_invite_users=True,
                    can_pin_messages=True
                )
                
                # Give full admin rights
                await bot.promote_chat_member(
                    chat_id, user_id,
                    is_anonymous=False,
                    can_manage_chat=True,
                    can_post_messages=True,
                    can_edit_messages=True,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_promote_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_manage_voice_chats=True
                )
                
                # Demote a user
                await bot.promote_chat_member(chat_id, user_id)
        """
        self.logger.info(f"Promoting user {user_id} in chat {chat_id}")
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "user_id": user_id
        }
        
        # Add optional parameters if provided
        if is_anonymous is not None:
            params["is_anonymous"] = json.dumps(is_anonymous)
            self.logger.info(f"Anonymous: {is_anonymous}")
        if can_manage_chat is not None:
            params["can_manage_chat"] = json.dumps(can_manage_chat)
            self.logger.info(f"Can manage chat: {can_manage_chat}")
        if can_post_messages is not None:
            params["can_post_messages"] = json.dumps(can_post_messages)
            self.logger.info(f"Can post messages: {can_post_messages}")
        if can_edit_messages is not None:
            params["can_edit_messages"] = json.dumps(can_edit_messages)
            self.logger.info(f"Can edit messages: {can_edit_messages}")
        if can_delete_messages is not None:
            params["can_delete_messages"] = json.dumps(can_delete_messages)
            self.logger.info(f"Can delete messages: {can_delete_messages}")
        if can_restrict_members is not None:
            params["can_restrict_members"] = json.dumps(can_restrict_members)
            self.logger.info(f"Can restrict members: {can_restrict_members}")
        if can_promote_members is not None:
            params["can_promote_members"] = json.dumps(can_promote_members)
            self.logger.info(f"Can promote members: {can_promote_members}")
        if can_change_info is not None:
            params["can_change_info"] = json.dumps(can_change_info)
            self.logger.info(f"Can change info: {can_change_info}")
        if can_invite_users is not None:
            params["can_invite_users"] = json.dumps(can_invite_users)
            self.logger.info(f"Can invite users: {can_invite_users}")
        if can_pin_messages is not None:
            params["can_pin_messages"] = json.dumps(can_pin_messages)
            self.logger.info(f"Can pin messages: {can_pin_messages}")
        if can_manage_voice_chats is not None:
            params["can_manage_voice_chats"] = json.dumps(can_manage_voice_chats)
            self.logger.info(f"Can manage voice chats: {can_manage_voice_chats}")
        
        # Make the API request
        return await self._promote_chat_member_request(params)
    
    async def _promote_chat_member_request(self, params: dict) -> bool:
        """Make the actual API request for promoting a user.
        
        Parameters:
            params (``dict``):
                Parameters to send in the request.
                
        Returns:
            ``bool``: True on success.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/promoteChatMember"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when promoting user: {await response.text()}")
                        return False
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error promoting user: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return False
                        
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 
import asyncio
import re
import datetime
import time
from aiogram.dispatcher.webhook import types
from aiogram.dispatcher.filters import ChatTypeFilter, RegexpCommandsFilter
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageNotModified

import db_methods as db
from helpers.bot import bot, dispatcher
from helpers.config import logger, config


@dispatcher.message_handler(ChatTypeFilter(types.ChatType.SUPERGROUP), content_types=types.ContentType.ANY)
@dispatcher.message_handler(ChatTypeFilter(types.ChatType.GROUP), content_types=types.ContentType.ANY)
@dispatcher.message_handler(ChatTypeFilter(types.ChatType.SUPERGROUP), RegexpCommandsFilter(regexp_commands=['.*']))
@dispatcher.message_handler(ChatTypeFilter(types.ChatType.GROUP), RegexpCommandsFilter(regexp_commands=['.*']))
async def group_message_handler(message: types.Message):
    # Ботов нафиг
    if message.left_chat_member:
        try:
            await bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            logger.exception(f'SHIT: {e}')
    elif message.new_chat_members:
        current_time = datetime.datetime.now()
        # Add 40 seconds to the current time
        future_time = current_time + datetime.timedelta(seconds=40)
        # Convert the future time to a Unix timestamp
        until_date = int(time.mktime(future_time.timetuple()))
        try:
            await bot.ban_chat_member(message.chat.id, message.new_chat_members[0].id, until_date=until_date, revoke_messages=False)
        except Exception as e:
            logger.exception(f'SHIT: {e}')
        try:
            await bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            logger.exception(f'SHIT: {e}')
        try:
            await bot.unban_chat_member(message.chat.id, message.new_chat_members[0].id, only_if_banned=True)
        except Exception as e:
            logger.exception(f'SHIT: {e}')

import asyncio
import traceback
from aiogram.dispatcher.webhook import types
from aiogram.types.chat import ChatActions
from textwrap import dedent

from helpers.consts import *
from helpers.config import logger, config
import db_methods as db
from helpers.bot import bot, dispatcher, reg_state, callbacks_processors, state_processors


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    logger.debug('start')

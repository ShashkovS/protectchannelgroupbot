'''
Здесь совершенно ужасный код.
Это стартовая версия веб-приложения в очень зачаточном состоянии.
Требуется большой рефакторинг
'''
from __future__ import annotations

import asyncio
import logging
import re
import time
from datetime import datetime

from aiohttp import web

from helpers.config import config, logger, DEBUG, APP_PATH
import db_methods as db

__ALL__ = ['routes', 'on_startup', 'on_shutdown']

routes = web.RouteTableDef()


async def on_startup(app):
    logger.debug('game on_startup')
    if __name__ == "__main__":
        # Настраиваем БД
        db.sql.setup(config.db_filename)


async def on_shutdown(app):
    logger.warning('game on_shutdown')
    if __name__ == "__main__":
        db.sql.disconnect()
    logger.warning('game web app Bye!')


def configue(app):
    app.add_routes(routes)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)


if __name__ == "__main__":
    # Включаем все отладочные сообщения
    SEND_OPEN_CHEST_TO_BOT = False
    logging.basicConfig(level=logging.DEBUG)
    logger.setLevel(DEBUG)
    # use_cookie = DEBUG_COOKIE
    app = web.Application()
    configue(app)
    print('Open http://127.0.0.1:8080/tester')
    web.run_app(app)

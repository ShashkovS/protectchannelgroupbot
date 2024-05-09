# -*- coding: utf-8 -*-
import logging
import os
import json
import pathlib
from dataclasses import dataclass
from typing import Union, Optional

APP_LOGGER = 'TeBot'
APP_PATH = pathlib.Path(__file__).parent.parent.resolve()
os.chdir(APP_PATH)

__all__ = ['APP_PATH', 'logger', 'config', 'DEBUG']


def _absolute_path(path: str) -> pathlib.Path:
    path_obj = pathlib.Path(path)
    if path_obj.is_absolute():
        return path_obj
    else:
        # Используем путь от корня проекта
        return APP_PATH / path


@dataclass()
class Config:
    config_name: str = ''
    telegram_bot_token: str = ''
    webhook_host: str = ''
    webhook_port: int = -1
    production_mode: bool = False
    db_filename: str = ''
    sos_channel: Union[str, int] = ''
    exceptions_channel: Union[str, int] = ''
    sentry_dsn: Optional[str] = ''
    set_admin_password: str = ''
    logging_level = logging.WARNING


def _create_logger():
    # Настраиваем
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s %(name)-8s: %(levelname)-8s %(message)s',
        datefmt='%Y-%d-%m %H:%M:%S'
    )
    logger = logging.getLogger(APP_LOGGER)
    return logger


def _setup(*, force_production=False):
    config = Config()
    logging.info(f'Current working dir: {os.getcwd()}')
    if force_production or os.environ.get('PROD', None) == 'true':
        logger.info('Настройки в режиме PRODUCTION!!!')
        config.production_mode = True
        config_filename = _absolute_path('../creds_prod/bot_config_prod.json')
    else:
        logging.info('Настройки в режиме test')
        config.production_mode = False
        config_filename = _absolute_path('../creds_test/bot_config_test.json')

    try:
        with open(config_filename, 'r') as f:
            config_from_json = json.load(f)
    except:
        logging.critical(f'Запишите конфиг в {config_filename} в формате\n'
                         '`{"telegram_bot_token": "...", "webhook_host": "host.ru", "webhook_port": 443, "db_filename": "test.db"}`')
        raise

    # Определяем абсолютный путь к БД
    config_from_json['db_filename'] = _absolute_path(config_from_json['db_filename'])

    # Обновляем настройки
    config.__dict__.update(config_from_json)
    return config


def _init_sentry(dsn: str, environment: str):
    # Добавляем отправку в sentry, если задан ключи
    if dsn:
        try:
            import sentry_sdk
            from sentry_sdk.integrations.aiohttp import AioHttpIntegration
            sentry_sdk.init(
                dsn=dsn,
                integrations=[AioHttpIntegration()],
                traces_sample_rate=1.0,
                environment=environment
            )
            logging.info('Sentry started')

        except:
            pass


logger = _create_logger()
DEBUG = logging.DEBUG
config = _setup()
_init_sentry(config.sentry_dsn, config.config_name)
logger.debug(f'{config=}')

if config.production_mode:
    logger.info(('*' * 50 + '\n') * 5)
    logger.info('Production mode')
    logger.info('*' * 50)
else:
    logger.info('Dev mode')

if __name__ == '__main__':
    print(config)
    print('-' * 50)
    # Тестируем sentry
    if config.sentry_dsn:
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warn message')
        logger.error('error message')
        try:
            a = [1][2]
        except:
            logger.exception('exception message')
        # Наконец-то валимся
        division_by_zero = 1 / 0

# -*- coding: utf-8 -*-
from enum import Enum, IntEnum, IntFlag, unique


# СОСТОЯНИЯ
# Важно, чтобы каждый state был уникальной числовой константой, которая больше никогда не меняется
# (так как она сохраняется в БД)
@unique
class STATE(IntEnum):
    GET_TITLE = 2
    GET_GENRE = 3
    GET_NAME = 4
    GET_TAGLINE = 5
    GET_REVIEW = 6
    GET_ACTORS = 9
    GET_POSTER = 7
    ASK_REPEAT = 8
    ALL_DONE = 10
    WAIT_SOS_REQUEST = 99



# ПРЕФИКСЫ ДАННЫХ ДЛЯ КОЛЛБЕКОВ
# Важно, чтобы константа была уникальной буквой (там хардкод взятия первой буквы)
# (наследование от str важно, чтобы условный CALLBACK.PROBLEM_SELECTED превращался в t, а не в своё длинное имя
@unique
class CALLBACK(str, Enum):
    RESET = 'r'
    BACK = 'B'
    # old
    PROBLEM_SELECTED = 't'
    SOS_PROBLEM_SELECTED = 'T'
    RATING = 'R'
    QUESTION = 'Q'
    OTHER_SOS = 'S'
    CANCEL = 'c'
    NOONBOARDING = 'n'
    ONBOARDING = 'o'
    OPENGAME = 'g'
    GRADE = 'G'
    NOGRADE = 'N'

    def __str__(self):
        return self.value


# ТИПЫ ПОЛЬЗОВАТЕЛЕЙ
@unique
class USER_TYPE(IntFlag):
    STUDENT = 1
    ADMIN = 128


# Статусы раундов
@unique
class ROUND_STATUS(IntEnum):
    BEFORE = 0
    OPEN = 1
    CLOSED = 2

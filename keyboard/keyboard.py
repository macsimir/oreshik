from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
 

from aiogram import types

def random_question_button():
    kb = [
        [
            types.KeyboardButton(text="новый вопрос"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=""
    )
    return keyboard

def mode_selection_start_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Случайный вопрос", callback_data="random_questions_F_key")],
        [types.InlineKeyboardButton(text="Вопросы на знание друг друга", callback_data="questions_for_friends_F_key")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def mode_selection_proverka_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Начать",callback_data="go_to_lobby_F_key")],
        [types.InlineKeyboardButton(text="Зайти в лобби", callback_data="connect_to_lobby_F_key"),
         types.InlineKeyboardButton(text="Создать лобби", callback_data="create_to_lobby_F_key")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# def choice_lobby_keuboard():
#     buttons = [
#         [types.InlineKeyboardButton(text="Зайти в лобби", callback_data="connect_to_lobby_F_key")],
#         [types.InlineKeyboardButton(text="Создать лобби", callback_data="create_to_lobby_F_key")]
#     ]
#     keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
#     return keyboard

def connect_to_lobby_choice_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Лобби №1", callback_data="lobby_1_F"),
         types.InlineKeyboardButton(text="Лобби №2", callback_data="lobby_2_F")],
        [types.InlineKeyboardButton(text="Лобби №3", callback_data="lobby_3_F"),
         types.InlineKeyboardButton(text="Лобби №4", callback_data="lobby_4_F"),],
         [types.InlineKeyboardButton(text="Лобби №5", callback_data="lobby_5_F"),
          types.InlineKeyboardButton(text="Назад", callback_data=""),]

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
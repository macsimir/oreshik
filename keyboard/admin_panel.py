from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_panel():
    buttons = [
        [types.InlineKeyboardButton(text="", callback_data="new appointment"), types.InlineKeyboardButton(text="Поменять аккаунт", callback_data="new_acc")],
        [types.InlineKeyboardButton(text="Активные заявки", callback_data="all_active_orders")]
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

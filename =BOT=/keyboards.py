from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

accept = InlineKeyboardButton(text='✔ Да', callback_data='accept')
deny = InlineKeyboardButton(text='❌ Нет', callback_data='deny')

approvalKB = InlineKeyboardMarkup(inline_keyboard=[[accept, deny]])
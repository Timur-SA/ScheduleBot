from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
router = Router()



@router.message(CommandStart())
async def start(message: Message):
    await message.reply(f"Привет!")


@router.message(Command("today"))
async def today(message: Message):
    await message.reply(f"Привет!")

@router.message(Command("tomorrow"))
async def tomorrow(message: Message):
    await message.reply(f"Привет!")

@router.message(Command("week"))
async def week(message: Message):
    await message.reply(f"Привет!")


@router.message(Command("add"))
async def add(message: Message):
    await message.reply(f"Привет!")


@router.message(Command("help"))
async def help(message: Message):
    await message.reply(f"Привет!")

@router.message(Command("schedule"))
async def schedule(message: Message):
    await message.reply(f"Привет!")
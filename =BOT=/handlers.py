from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import data
router = Router()


@router.message(CommandStart())
async def start(msg: Message):
    await msg.reply(f"Привет!")


@router.message(Command("today"))
async def today(msg: Message):
    await msg.reply(f"Привет!")
    data.getEventsbyDay(data.loadData())

@router.message(Command("tomorrow"))
async def tomorrow(msg: Message):
    await msg.reply(f"Привет!")

@router.message(Command("week"))
async def week(msg: Message):
    await msg.reply(f"Привет!")


@router.message(Command("add"))
async def add(msg: Message, cmd : Command):
    await msg.reply(f"Привет!")


@router.message(Command("help"))
async def help(msg: Message):
    await msg.reply(f"Привет!")

@router.message(Command("schedule"))
async def schedule(msg: Message):
    await msg.reply(f"Привет!")
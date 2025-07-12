from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import re
import data
router = Router()


@router.message(CommandStart())
async def start(msg: Message):
    await msg.reply(f"Привет!")


@router.message(Command("today"))
async def today(msg: Message):
    events = data.getDayData(data.loadGlobalFile())
    await msg.answer(data.prepareDayMessage(events))
    
@router.message(Command("tomorrow"))
async def tomorrow(msg: Message):
    events = data.getDayData(data.loadGlobalFile(), 1)
    await msg.answer(data.prepareDayMessage(events))

@router.message(Command("week"))
async def week(msg: Message): pass

@router.message(Command("days"))
async def days(msg: Message): print(data.getDays(data.loadGlobalFile()))    


@router.message(Command("add"))
async def add(msg: Message):
    if(re.match(r"^/add (.+?) (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})$", msg.text)):
        await msg.answer("Yes")
        args = msg.text.split()[1:]
        data.writeEvent(args, msg.from_user.id)
    else:
        await msg.answer("No")


@router.message(Command("help"))
async def help(msg: Message):
    await msg.reply(f"Привет!")

@router.message(Command("schedule"))
async def schedule(msg: Message):
    await msg.reply(f"Привет!")
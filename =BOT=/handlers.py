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
    events = data.getDayData(data.loadData())
    eventsMessages = []
    for event in events:
        eventsMessages.append(f"{event['time']} - {event['name']}\n")
    
    if(eventsMessages):
        await msg.answer("".join(eventsMessages))
    else:
        await msg.answer("На этот день у вас ничего не запланировано! 😉")

@router.message(Command("tomorrow"))
async def tomorrow(msg: Message):
    events = data.getDayData(data.loadData(), 1)
    eventsMessages = []
    for event in events:
        eventsMessages.append(f"{event['time']} - {event['name']}\n")
    
    if(eventsMessages):
        await msg.answer("".join(eventsMessages))
    else:
        await msg.answer("На этот день у вас ничего не запланировано! 😉")

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
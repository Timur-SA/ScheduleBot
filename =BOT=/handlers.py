from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import re
import data
router = Router()


def getEvents(deltaDays=0):
    events = data.getDayData(data.loadGlobalFile(), deltaDays)
    if events:
        return "\n".join(["📝 События:", data.prepareDayMessage(events)])
    else:
        return "📝 События отсутствуют!"

def getNotifications(uid, deltaDays=0):
    notifications = data.getDayData(data.loadLocalFile(uid), deltaDays)
    if notifications:
        return "\n".join(["🔔 Напоминания:", data.prepareDayMessage(notifications)])
    else:
        return "🔔 Напоминания отсутствуют"


@router.message(CommandStart())
async def start(msg: Message):
    await msg.reply(f"Привет! Я - бот планировщик задач\nУ меня есть команды /help и /schedule, которые помогут тебе создать своё первое напоминание!")


@router.message(Command("today"))
async def today(msg: Message):
    await msg.answer(getEvents())
    await msg.answer(getNotifications(msg.from_user.id))
    
@router.message(Command("tomorrow"))
async def tomorrow(msg: Message):
    await msg.answer(getEvents(deltaDays=1))
    await msg.answer(getNotifications(msg.from_user.id, deltaDays=1))

@router.message(Command("week"))
async def week(msg: Message): pass


@router.message(Command("add"))
async def add(msg: Message):
    if(re.match(r"^/add (.+?) (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})$", msg.text)):
        args = msg.text.split()[1:]
        status = data.writeEvent(args, msg.from_user.id)

        if(status=="OK"): await msg.answer("🔔 Напоминание успешно добавлено!")
        elif(status=="replacement"): await msg.answer("🔄 Напоминание отредактировано!")
        elif(status=="unactual"): await msg.answer("😅 Время напоминания уже прошло")
        else: raise RuntimeError()

    else:
        await msg.answer("❗ Неверный формат напоминания!")
        await msg.answer("Добавить своё напоминание: `/add Название напоминания ГГГГ-ММ-ДД чч:мм`", parse_mode="markdown")


@router.message(Command("help"))
async def help(msg: Message):
    await msg.reply(f"""/today - Вывести события на сегодня
/tomorrow - Вывести события на завтра
/week - Вывести расписание событий на всю неделю
/add - Добавить своё событие (`/add [Название] <ГГГГ-ММ-ДД> <чч:мм>`)
/help - Список доступных команд 
/schedule - Инструкция к команде /add (добавить событие)""",
parse_mode="markdown")

@router.message(Command("schedule"))
async def schedule(msg: Message):
    await msg.reply(f"-Как добавить своё напоминание?\n/add (Название) (Дата в формате: <ГГГГ-ММ-ДД>) (Время в формате: <чч:мм>)\nПример: `/add Ваше первое напоминание!🥳 2025-07-31 15:00`", parse_mode="markdown")
from aiogram import Router
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import re
from datetime import datetime
import data, keyboards as kb, reminders
from botInstance import bot
router = Router()
deleteState = State()


def getEventsbyDay(deltaDays=0):
    events = data.getDayData(data.loadGlobalFile(), deltaDays)
    if events:
        return "\n".join(["📝 События:", data.prepareDayMessage(events)])
    else:
        return "📝 События отсутствуют!"

def getNotificationsbyDay(uid, deltaDays=0):
    notifications = data.getDayData(data.loadLocalFile(uid), deltaDays)
    if notifications:
        return "\n".join(["🔔 Напоминания:", data.prepareDayMessage(notifications)])
    else:
        return "🔔 Напоминания отсутствуют"


@router.callback_query(lambda q: q.data == 'accept')
async def accept(cq: CallbackQuery, state: FSMContext):
    stateData = await state.get_data()
    delDate = stateData.get("date")
    delTime = stateData.get("time")

    data.deleteNotification([delDate, delTime], cq.from_user.id)
    await cq.message.edit_text('🗑 Напоминание удалено')
    await state.clear()

@router.callback_query(lambda q: q.data == 'deny')
async def accept(cq: CallbackQuery, state: FSMContext):
    await cq.message.edit_text('Удаление отменено!')
    await state.clear()


@router.message(CommandStart())
async def start(msg: Message):
    events = data.getEvents(data.loadGlobalFile())
    await msg.reply(f"Привет! Я - бот планировщик задач\nУ меня есть команды /help и /schedule, которые помогут тебе создать своё первое напоминание!")
    for event in events:
        reminders.scheduleReminder(msg.chat.id, datetime.fromisoformat(f"{event['day']}T{event['time']}"), [1], notification, "📝 Скоро произойдёт событие!", "📝 Событие началось!", event["name"]) 


@router.message(Command("today"))
async def today(msg: Message):
    await msg.answer(getEventsbyDay())
    await msg.answer(getNotificationsbyDay(msg.from_user.id))
    
@router.message(Command("tomorrow"))
async def tomorrow(msg: Message):
    await msg.answer(getEventsbyDay(deltaDays=1))
    await msg.answer(getNotificationsbyDay(msg.from_user.id, deltaDays=1))

@router.message(Command("week"))
async def week(msg: Message): pass


@router.message(Command("add"))
async def add(msg: Message):
    if(re.match(r"^/add (.+?) (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})$", msg.text)):
        args = msg.text.split()[1:]
        status = data.writeNotification(args, msg.from_user.id)

        if(status=="OK"): 
            await msg.answer("🔔 Напоминание успешно добавлено!")
            reminders.scheduleReminder(msg.chat.id, datetime.fromisoformat(f"{args[-2]}T{args[-1]}"), [1], notification, "🔔 Скоро сработает напоминание!", "🔔 Сработало напоминание!", " ".join(args[:-2]))

        elif(status=="replacement"): 
            await msg.answer("🔄 Напоминание отредактировано!")
            reminders.scheduleReminder(msg.chat.id, datetime.fromisoformat(f"{args[-2]}T{args[-1]}"), [1], notification, "🔔 Скоро сработает напоминание!", "🔔 Сработало напоминание!", " ".join(args[:-2]))

        
        elif(status=="unactual"): await msg.answer("😅 Время напоминания уже прошло")
        else: raise RuntimeError("Status invalid")

    else:
        await msg.answer("❗ Неверный формат напоминания!")
        await msg.answer("Добавить своё напоминание: `/add Название напоминания ГГГГ-ММ-ДД чч:мм` 👈", parse_mode="markdown")

@router.message(Command("del", "delete"))
async def delete(msg: Message, state = FSMContext):
    if(re.match(r"^/del (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})$", msg.text)):
        args = msg.text.split()[1:]
        status, notificationName = data.findNotification(msg.from_user.id, args[0], args[1])

        if(status):
            await state.set_state(deleteState)
            await state.update_data(date=args[0], time=args[1])

            await msg.answer(f"❓ Вы уверены, что хотите удалить напоминание {notificationName}?", reply_markup=kb.approvalKB)
        else:
            await msg.answer("❗ Напоминание не найдёно, проверьте правильность ввода!")
    else:
        await msg.answer("❗ Неверный формат!")
        await msg.answer("Удалить напоминание: `/del ГГГГ-ММ-ДД чч:мм` 👈", parse_mode="markdown")


@router.message(Command("help"))
async def help(msg: Message):
    await msg.reply(f"""/today - Вывести события на сегодня
/tomorrow - Вывести события на завтра
/week - Вывести расписание событий на всю неделю
/add - Добавить своё событие (`/add [Название] <ГГГГ-ММ-ДД> <чч:мм>` 👈)
/help - Список доступных команд 
/schedule - Инструкция к команде /add (добавить событие)""",
parse_mode="markdown")

@router.message(Command("schedule"))
async def schedule(msg: Message):
    await msg.reply(f"-Как добавить своё напоминание?\n/add (Название) (Дата в формате: <ГГГГ-ММ-ДД>) (Время в формате: <чч:мм>)\nПример: `/add Ваше первое напоминание!🥳 2025-07-31 15:00` 👈", parse_mode="markdown")


async def notification(cid, notificationTime, msgText, notificationName):
    await bot.send_message(cid, f"{msgText}\n{notificationTime} - {notificationName}")
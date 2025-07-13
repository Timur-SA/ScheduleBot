import asyncio
from aiogram import Dispatcher
from aiogram.exceptions import TelegramNetworkError

from handlers import router
from reminders import scheduler
from botInstance import bot

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    scheduler.start()
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    try:
        print("✅ Бот включается")
        asyncio.run(main())
        

    except KeyboardInterrupt:
        print("🚫 Бот выключается")
    except TelegramNetworkError:
        print("Соеденение потеряно...")
else:
    print("⚠ Бот запущен через диспетчер обновлений / Ошибка импорта")
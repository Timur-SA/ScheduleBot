import asyncio
from aiogram import Bot, Dispatcher

from handlers import router

async def main():
    bot = Bot(token="7398610094:AAE6mwRAO3nWxHm61Xil_GvJds1TAK1WR-Y")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        print("✅ Бот включается")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🚫 Бот выключается")
else:
    print("⚠ Бот запущен через диспетчер / Ошибка импорта")
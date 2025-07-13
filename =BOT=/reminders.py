from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta

jobstore = SQLAlchemyJobStore(url='sqlite:///notifications.sqlite')
scheduler = AsyncIOScheduler(jobstores={'default': jobstore})

def scheduleReminder(cid, notificationDate:datetime, notificationDeltas:list[int], func, beforeText, actualText, eventName:str):

    for deltaTime in notificationDeltas:
        runDate = notificationDate-timedelta(hours=deltaTime)
        if not(runDate <= datetime.now()):
           print(f"Ставится работа на {notificationDate-timedelta(hours=deltaTime)}")
           scheduler.add_job(
            func, 'date', run_date=notificationDate-timedelta(hours=deltaTime), args=[cid, notificationDate.time(), beforeText, eventName]
            )
    
    print(f"Ставится работа на {notificationDate}")
    scheduler.add_job(func, 'date', run_date=notificationDate, args=[cid, notificationDate.time(), actualText, eventName])
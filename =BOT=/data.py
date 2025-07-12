import json
from datetime import datetime, timedelta
from sys import argv as _argv
from os import path as _path

localDir = _path.dirname(_argv[0])


def loadData(name="global"):
    with open(_path.join(localDir, "DataTables", f"{name}.json"), "r", encoding="utf-8") as jsonFile:
        return json.load(jsonFile)

def getDays(dataTable): 
    for day in dataTable:
        print(f"{day}")

def getDayData(dataTable, delta = 0):
    if(delta < 0): print("Runtime Warning: Delta < 0!")

    eventsDay = datetime.now().date()
    eventsDay += timedelta(delta)


    #events = dataTable.get("2025-07-13", [])
    day = dataTable.get(eventsDay.strftime("%Y-%m-%d"), [])
    return day


def prepareDayMessage(eventsList):
    eventsMessages = []
    for event in eventsList:
        eventsMessages.append(f"{event['time']} - {event['name']}\n")
    
    if(eventsMessages):
        return "".join(eventsMessages)
    else:
        return "На этот день у вас ничего не запланировано! 😉"
    
def prepareSchedule(days):
    pass


def prepareWeekInterval():
    pass
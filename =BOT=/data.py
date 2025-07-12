import json
from datetime import datetime, timedelta
from sys import argv as _argv
from os import path as _path

localDir = _path.dirname(_argv[0])


def loadGlobalFile():
    with open(_path.join(localDir, "DataTables", "global.json"), "r", encoding="utf-8") as jsonFile:
        return json.load(jsonFile)

# def loadLocalFile(filename):
#     try:
#         with open(_path.join(localDir, "DataTables", f"{filename}.json"), "r+", encoding="utf-8") as jsonFile:
#             return json.load(jsonFile)
#     except FileNotFoundError:
#         with open(_path.join(localDir, "DataTables", f"{filename}.json"), "w", encoding="utf-8") as jsonFile:
#             json.dump({}, jsonFile, ensure_ascii=False, indent=2)
#             return json.load(jsonFile)

def getDays(dataTable): 
    for day in dataTable:
        print(f"{day}")

def getDayData(dataTable, delta = 0):
    if(delta < 0): print("Runtime Warning: Delta < 0!")

    eventsDay = datetime.now().date()
    eventsDay += timedelta(delta)


    day = dataTable.get(eventsDay.strftime("%Y-%m-%d"), [])
    return day


def writeEvent(addArgs:list[str], username):
    # localFile = loadLocalFile(username)

    # print(localFile)
    # localFile[addArgs[-2]] = {"time": addArgs[-1], "name": addArgs[:-2]}
    # print(localFile)
    try:
        with open(_path.join(localDir, "DataTables", f"{username}.json"), "r+", encoding="utf-8") as jsonFile:
            return json.load(jsonFile)
    except FileNotFoundError:
        with open(_path.join(localDir, "DataTables", f"{username}.json"), "w", encoding="utf-8") as jsonFile:
            json.dump(
                {addArgs[-2]: 
                [{"time": addArgs[-1],
                  "name": " ".join(addArgs[:-2])}]
                },
                jsonFile, ensure_ascii=False, indent=2)


def writeFile(filename, file):
    pass

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
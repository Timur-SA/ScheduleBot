import json
from datetime import datetime, timedelta
from sys import argv as _argv
from os import path as _path

localDir = _path.dirname(_argv[0])


def loadGlobalFile():
    with open(_path.join(localDir, "DataTables", "global.json"), "r", encoding="utf-8") as jsonFile:
        return json.load(jsonFile)

def loadLocalFile(filename):
    try:
        with open(_path.join(localDir, "DataTables", f"{filename}.json"), "r", encoding="utf-8") as jsonFile:
            return json.load(jsonFile)
    except FileNotFoundError:
        return []


def getDays(dataTable): 
    for day in dataTable:
        print(f"{day}")

def getDayData(dataTable, delta = 0)-> dict: 
    if(delta < 0): raise(RuntimeWarning("Delta is < 0!"))

    eventsDay = datetime.now().date()
    eventsDay += timedelta(delta)


    day = dataTable.get(eventsDay.strftime("%Y-%m-%d"))
    return day


def writeEvent(addArgs:list[str], username):
    eventDay = addArgs[-2]
    eventTime = addArgs[-1]
    eventName = addArgs[:-2]
    
    try:
        with open(_path.join(localDir, "DataTables", f"{username}.json"), "r+", encoding="utf-8") as jsonFile:
            try:
                jsonData = json.load(jsonFile)
                _recoveryData = jsonData
                jsonFile.seek(0)  
                jsonFile.truncate() 

                if eventDay in jsonData:
                    jsonData[eventDay].append(
                        {"time": eventTime,
                        "name": " ".join(eventName)})
                else:
                    jsonData[eventDay] = [{
                        "time": eventTime,
                        "name": " ".join(eventName)}]
                jsonData[eventDay] = sorted(jsonData[eventDay], key=lambda x: x['time'])
                json.dump(jsonData, jsonFile, ensure_ascii=False, indent=2)

            except Exception:
                json.dump(_recoveryData, jsonFile, ensure_ascii=False, indent=2)
                raise RuntimeWarning("Write event into JSON failure")

    except FileNotFoundError:
        with open(_path.join(localDir, "DataTables", f"{username}.json"), "w", encoding="utf-8") as jsonFile:
            json.dump(
                {addArgs[-2]: 
                [{"time": addArgs[-1],
                  "name": " ".join(addArgs[:-2])}]
                },
                jsonFile, ensure_ascii=False, indent=2)


def prepareDayMessage(eventsList):
    eventsMessages = []
    for event in eventsList:
        eventsMessages.append(f"{event['time']} - {event['name']}\n")
    
    if(eventsMessages):
        print(eventsMessages)
        return "".join(eventsMessages)
    else:
        return "На этот день у вас ничего не запланировано! 😉"
    
def prepareSchedule(days):
    pass

def prepareWeekInterval():
    pass
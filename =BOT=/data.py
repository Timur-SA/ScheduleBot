import json
from datetime import datetime, timedelta
from config import localPath, path

def loadGlobalFile():
    with open(path.join(localPath, "DataTables", "global.json"), "r", encoding="utf-8") as jsonFile:
        return json.load(jsonFile)

def loadLocalFile(filename):
    try:
        with open(path.join(localPath, "DataTables", f"{filename}.json"), "r", encoding="utf-8") as jsonFile:
            return json.load(jsonFile)
    except FileNotFoundError:
        return {}


def getEvents(dataTable):
    events = []
    for day in dataTable:
        for event in dataTable[day]:
            event.update({"day": day})
            events.append(event)
    return events

def getDayData(dataTable, delta = 0)-> dict: 
    if(delta < 0): raise(RuntimeWarning("Delta is < 0!"))

    eventsDay = datetime.now().date()
    eventsDay += timedelta(delta)

    
    day = dataTable.get(eventsDay.strftime("%Y-%m-%d"))
    return day


def findNotification(uid, day, time):
    localData = loadLocalFile(uid)
    if day in localData:
        events = [event for event in localData[day] if event["time"] == time]

        if events: return True, events[0]["name"]
        else:      return False, None

    else: return False, None
            

def writeNotification(addArgs:list[str], uid)->str:
    eventDay = addArgs[-2]
    eventTime = addArgs[-1]
    eventName = addArgs[:-2]
    
    try:
        with open(path.join(localPath, "DataTables", f"{uid}.json"), "r+", encoding="utf-8") as jsonFile:
            _recoveryData = {}
            try:
                eventStatus = validateDate(eventDay, eventTime, uid)

                if eventStatus in ("OK", "replacement"):
                    jsonData = json.load(jsonFile)
                    _recoveryData = jsonData
                    jsonFile.seek(0)  
                    jsonFile.truncate() 

                    if eventDay in jsonData:
                        if eventStatus == "OK": 
                            jsonData[eventDay].append(
                                {"time": eventTime,
                                "name": " ".join(eventName)})
                        else:
                            jsonData[eventDay] = [exlEvents for exlEvents in jsonData[eventDay] if exlEvents["time"] != eventTime]
                            jsonData[eventDay].append(
                                {"time": eventTime,
                                "name": " ".join(eventName)})
                    else:
                        jsonData[eventDay] = [{
                            "time": eventTime,
                            "name": " ".join(eventName)}]
                    jsonData[eventDay] = sorted(jsonData[eventDay], key=lambda x: x['time'])
                    json.dump(jsonData, jsonFile, ensure_ascii=False, indent=2)
                    
                    return eventStatus
                
                else: return eventStatus

            except Exception:
                json.dump(_recoveryData, jsonFile, ensure_ascii=False, indent=2)
                raise RuntimeWarning("Write event into JSON failure")

    except FileNotFoundError:
        with open(path.join(localPath, "DataTables", f"{uid}.json"), "w", encoding="utf-8") as jsonFile:
            eventStatus = "OK"
            json.dump(
                {addArgs[-2]: 
                [{"time": addArgs[-1],
                  "name": " ".join(addArgs[:-2])}]
                },
                jsonFile, ensure_ascii=False, indent=2)
            return "OK"

def deleteNotification(delArgs:list[str], uid):
    dataTable = loadLocalFile(uid)
    delDay = delArgs[0]
    delTime = delArgs[1]

    dataTable[delDay] = [event for event in dataTable.get(delDay) if event["time"] != delTime]
    
    with open(path.join(localPath, "DataTables", f"{uid}.json"), "w", encoding="utf-8") as jsonFile:
        json.dump(dataTable, jsonFile, ensure_ascii=False, indent=2)


def prepareDayMessage(eventsList):
    eventsMessages = []
    for event in eventsList:
        eventsMessages.append(f"{event['time']} - {event['name']}\n")
    
    if(eventsMessages):
        return "".join(eventsMessages)
    else:
        return "На этот день у вас ничего не запланировано! 😉"


def validateDate(day, time, username)->str:
    date = datetime.fromisoformat(f"{day}T{time}")
    if(date < datetime.now()):
        return "unactual"
    
    status, _name = findNotification(username, day, time)
    if status:
        return "replacement"
    else:
        return "OK"
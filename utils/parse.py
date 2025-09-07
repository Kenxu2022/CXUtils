from pydantic import BaseModel
import time

class parseCourseResult(BaseModel):
    name: str
    teacher: str
    courseID: int
    classID: int

class ParseActivityResult(BaseModel):
    name: str
    startTime: str
    endTime: str
    active: bool
    id: int
    activeType: int

def parseCourse(data: dict):
    courseList = []
    for item in data["channelList"]:
        courseList.append(parseCourseResult(
            name = item["content"]["course"]["data"][0]["name"], 
            teacher = item["content"]["course"]["data"][0]["teacherfactor"], 
            courseID = item["content"]["course"]["data"][0]["id"], 
            classID = item["content"]["id"]
        ))
    return {
        "success": True,
        "data": courseList
    }

def parseActivity(data: dict):
    activityList = []
    for item in data["data"]["activeList"]:
        if item["activeType"] != 2: # skip non signin activity
            continue     
        startTime = time.localtime(float(item["startTime"]) / 1000)
        endTime = time.localtime(float(item["endTime"]) / 1000)
        activityList.append(ParseActivityResult(
            name = item["nameOne"],
            startTime = str(time.strftime("%Y-%m-%d %H:%M:%S", startTime)),
            endTime = str(time.strftime("%Y-%m-%d %H:%M:%S", endTime)),
            active = True if item["status"] == 1 else False,
            id = item["id"],
            activeType = item["activeType"]
        ))      
    return {
        "success": True,
        "data": activityList
    }

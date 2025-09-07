from pydantic import BaseModel
import time
import json

class parseCourseResult(BaseModel):
    name: str
    teacher: str
    courseID: int
    classID: int

class parseActivityResult(BaseModel):
    name: str
    startTime: str
    endTime: str
    active: bool
    activeID: int
    activeType: int

class parseSignInDetailResult(BaseModel):
    type: int
    needValidation: bool

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
        activityList.append(parseActivityResult(
            name = item["nameOne"],
            startTime = str(time.strftime("%Y-%m-%d %H:%M:%S", startTime)),
            endTime = str(time.strftime("%Y-%m-%d %H:%M:%S", endTime)),
            active = True if item["status"] == 1 else False,
            activeID = item["id"],
            activeType = item["activeType"]
        ))      
    return {
        "success": True,
        "data": activityList
    }

def parseSignInDetail(data: dict):
    signInDetail = {
        "type": data['data']['otherId'], # 0-normal, 2-QRCode, 3-gesture, 4-location, 5-signcode
        "needValidation": True if data['data']['ifNeedVCode'] == 1 else False
    }
    return {
        "success": True,
        "detail": signInDetail
    }

def parseSignIn(data: str):
    if data == "success":
        return {
            "success": True,
            "detail": None
        }
    else:
        try: 
            data = json.loads(data)
            if data['result'] == 1:
                return {
                    "success": True,
                    "detail": None
                }
            else:
                {
                    "success": False,
                    "detail": data
                }
        except:
            return {
                "success": False,
                "detail": data
            }
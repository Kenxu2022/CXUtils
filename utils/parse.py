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

class parseQuizProblemResult(BaseModel):
    title: str
    type: int
    options: dict

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

def parseActivity(data: dict, activeType: list):
    """
    2：签到
    4：抢答
    5：主题讨论
    14：问卷
    35：分组任务
    42：随堂练习
    43：投票
    45：通知
    """
    activityList = []
    for item in data["data"]["activeList"]:
        if item["activeType"] not in activeType:
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

def parseServerTime(data: str):
    # remove cx_captcha_function()
    json_start = data.find("(") + 1
    json_end = data.rfind(")")
    data = json.loads(data[json_start:json_end])
    return data['t']

def parseCaptchaImageUrl(data: str):
    # remove cx_captcha_function()
    jsonStart = data.find("(") + 1
    jsonEnd = data.rfind(")")
    data = json.loads(data[jsonStart:jsonEnd])
    token = data["token"]
    slideImage = data["imageVerificationVo"]["cutoutImage"]
    backgroundImage = data["imageVerificationVo"]["shadeImage"]
    return [token, slideImage, backgroundImage]

def parseValidateCode(data: str):
    # remove cx_captcha_function()
    jsonStart = data.find("(") + 1
    jsonEnd = data.rfind(")")
    authData = json.loads(data[jsonStart:jsonEnd])
    if authData['result'] == True:
        validate = json.loads(authData['extraData'])['validate']
        return {
            "success": True,
            "code": validate
        }
    else:
        return None

def parseQuizProblem(data: dict):
    """
    0：单选
    1：多选
    2：填空
    4：简答
    16：判断
    """
    title = data["data"]["questionlist"][0]["content"][3:-4] # remove html tag
    type = data["data"]["questionlist"][0]["type"]
    originalData = data["data"]["questionlist"][0]
    options = {}
    for item in data["data"]["questionlist"][0]["answer"]:
        options[item["name"]] = item["content"][3:-4] # remove html tag
    return {
        "success": True,
        "data": parseQuizProblemResult(title = title, type = type, options = options),
        "originalData": originalData
    }

from pydantic import BaseModel
from typing import Optional
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
    options: Optional[dict]
    resourceUrl: Optional[list]

class parseDiscussionResult(BaseModel):
    content: str
    publicURL: str
    uuid: str
    bbsid: str

class parseReplyResult(BaseModel):
    floor: str
    name: str
    content: str

class parseBuzzInAttendList(BaseModel):
    name: str
    answerTime: str

class parseBuzzInResult(BaseModel):
    attendList: list[parseBuzzInAttendList]
    startTime: str
    endTime: str
    hasEnded: bool
    allowAnswerStuNum: int

def parseCourse(data: dict):
    courseList = []
    if data["result"] == 0:
        return {
            "success": False,
            "data": data["msg"]
        }
    for item in data["channelList"]:
        if item["content"].get("course") is None:
            continue
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

def parseUploadImage(data: dict):
    if data["result"]:
        return {
            "success": True,
            "detail": None,
            "objectId": data["objectId"]
        }
    else:        
        return {
            "success": False,
            "detail": data["msg"],
            "objectId": None
        }

def parseSignInDetail(data: dict):
    signInDetail = {
        "type": data['data']['otherId'], # 0-normal, 2-QRCode, 3-gesture, 4-location, 5-signcode
        "needValidation": True if data['data']['ifNeedVCode'] == 1 else False,
        "needLocation": True if data['data']['locationText'] else False,
        "needPhoto": True if data['data']['ifphoto'] == 1 else False
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
                errorMessage = data['errorMsg']
                return {
                    "success": False,
                    "detail": errorMessage
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
    quizList = []
    originalDataList = []
    for originalData in data["data"]["questionlist"]:
        title = originalData["content"][3:-4] # remove html tag
        type = originalData["type"]
        if not originalData["answer"][0]:
            options = None
        else:
            options = {}
            for item in originalData["answer"]:
                options[item["name"]] = item["content"][3:-4] if type in (0, 1) else item["content"] # remove html tag if necessary
        if not originalData["recArray"]:
            resourceUrl = None
        else:
            resourceUrl = []
            for urlData in originalData["recArray"]:
                resourceUrl.append(f"https://p.cldisk.com/star4/{urlData['objectid']}/origin.jpg")
        quizList.append(parseQuizProblemResult(title = title, type = type, options = options, resourceUrl = resourceUrl))
        originalDataList.append(originalData)
    return {
        "success": True,
        "data": quizList,
        "originalData": originalDataList
    }

def parseSubmitResult(data: dict):
    if data["result"] == 1:
        return {
            "success": True,
            "detail": None
        }
    else:
        return {
            "success": False,
            "detail": data["errorMsg"]
        }

def parseDiscussion(data: dict):
    content = data['datas']['text_content']
    publicURL = data['datas']['shareUrl']
    uuid = data['datas']['uuid']
    bbsid = data['datas']['bbsid']
    return {
        "success": True,
        "data": parseDiscussionResult(content = content, publicURL = publicURL, uuid = uuid, bbsid = bbsid)
    }

def parseReply(data: dict):
    replyList = []
    for r in data["data"]["datas"]:
        replyFloor = r['floor']
        replyName = r['creater_name']
        replyContent = r['content'].strip()
        replyList.append(parseReplyResult(floor = replyFloor, name = replyName, content = replyContent))
    return {
        "success": True,
        "data": replyList
    }

def parseReplyResponse(data: dict):
    replyStatus = data['status']
    serverMessage = data['msg']
    if replyStatus:
        return {
            "success": True,
            "data": None
        }
    else:
        return {
            "success": False,
            "data": serverMessage
        }
    
def parseBuzzIn(data: dict):
    attendList = []
    for item in data["data"]["attendList"]:
        name = item["name"]
        answerTime = item["answerTime"]
        attendList.append(parseBuzzInAttendList(name = name, answerTime = answerTime))
    startTime = data["data"]["pptActive"]["starttimeStr"]
    endTime = data["data"]["pptActive"]["endtimeStr"]
    hasEnded = True if data["data"]["pptActive"]["status"] == 2 else False
    configJson = json.loads(data["data"]["pptActive"]["configJson"])
    allowAnswerStuNum = configJson["allowAnswerStuNum"]
    return {
        "success": True,
        "data": parseBuzzInResult(attendList = attendList, startTime = startTime, endTime = endTime, hasEnded = hasEnded, allowAnswerStuNum = allowAnswerStuNum)
    }

def parseSubmitBuzzIn(data: dict):
    if data["result"] == 1:
        return {
            "success": True,
            "detail": None
        }
    else:
        return {
            "success": False,
            "detail": data["msg"]
        }
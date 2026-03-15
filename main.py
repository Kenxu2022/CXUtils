from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import uvicorn
from pydantic import BaseModel
from typing import Annotated, Optional
from configparser import ConfigParser
import os

from credentials.cookie import initializeCookie, getCookie, deleteCookie
from credentials.db import DatabaseManager
from auth import createToken,validateToken
from api import ChaoxingAPI, SignIn, Quiz, Discussion
from utils.parse import parseCourse, parseActivity, parseSignInDetail, parseSignIn, parseQuizProblem, parseSubmitResult, parseDiscussion, parseReply, parseReplyResponse
from utils.validate import generateValidateCode

class Token(BaseModel):
    access_token: str
    token_type: str

conf = ConfigParser()
conf.read('config.ini')
listenIP = os.getenv("LISTEN_IP", conf['API']['ListenIP'])
listenPort = int(os.getenv("LISTEN_PORT", conf['API']['Port']))
allowUserSync = os.getenv("ALLOW_USER_SYNC", conf['API']['AllowUserSync']).lower() == "true"
app = FastAPI(docs_url=None, redoc_url=None)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def getUser(token: Annotated[str, Depends(oauth2_scheme)]):
    user = validateToken(token)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.post("/token")
def userAuth(credential: Annotated[OAuth2PasswordRequestForm, Depends()]):
    result = createToken(credential.username, credential.password)
    if result:
        return Token(
            access_token = result,
            token_type = "bearer"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post("/addCredential")
def addCredential(username: str = Body(...), password: str = Body(...), nickname: str = Body(...), _ = Depends(getUser)):
    result = initializeCookie(username, password, nickname, False)
    result.pop('cookie')
    return result

@app.post("/deleteCredential")
def deleteCredential(username: str = Body(..., embed=True), _ = Depends(getUser)):
    result = deleteCookie(username)
    return result

@app.post("/syncUsers")
def syncUsers(_ = Depends(getUser)):
    if not allowUserSync:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User synchronization is disabled",
        )
    with DatabaseManager() as db:
        users = db.getUsers()
    return {
        "success": True,
        "data": users
    }

@app.post("/updateNickname")
def updateNickname(username: str = Body(...), nickname: str = Body(...), _ = Depends(getUser)):
    with DatabaseManager() as db:
        db.updateNickname(username, nickname)
    return {
        "success": True,
        "detail": None
    }

@app.post("/getCourse")
def getCourse(username: str = Body(..., embed=True), _ = Depends(getUser)):
    cookie = getCookie(username).get("cookie")
    result = ChaoxingAPI(cookie).getCourse()
    return parseCourse(result)

@app.post("/getActivity")
def getActivity(
    username: str = Body(...), 
    courseID: str = Body(...), 
    classID: str = Body(...), 
    activityType: list = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = ChaoxingAPI(cookie).getActivity(courseID, classID)
    return parseActivity(result, activityType)

@app.post("/getSignInDetail")
def getSignInDetail(
    username: str = Body(...), 
    activeID: str = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = SignIn(activeID, cookie).getMiscInfo()
    return parseSignInDetail(result)

@app.post("/getValidateCode")
def getValidateCode(
    username: str = Body(...), 
    courseID: str = Body(...), 
    classID: str = Body(...), 
    activeID: str = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    return generateValidateCode(cookie, courseID, classID, activeID)

@app.post("/normalSignIn")
def normalSignIn(
    username: str = Body(...),
    activeID: str = Body(...),
    validate: Optional[str] = Body(""),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = SignIn(activeID, cookie, validate).normalSignIn()
    return parseSignIn(result)

@app.post("/locationSignIn")
def locationSignIn(
    username: str = Body(...), 
    activeID: str = Body(...),
    locationText: str = Body(...),
    locationLatitude: str = Body(...),
    locationLongitude: str = Body(...),
    validate: Optional[str] = Body(""),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = SignIn(activeID, cookie, validate).locationSignIn(locationText, locationLatitude, locationLongitude)
    return parseSignIn(result)

@app.post("/qrcodeSignIn")
def qrcodeSignIn(
    username: str = Body(...), 
    activeID: str = Body(...),
    enc: str = Body(...),
    locationText: Optional[str] = Body(""),
    locationLatitude: Optional[str] = Body(""),
    locationLongitude: Optional[str] = Body(""),
    validate: Optional[str] = Body(""),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = SignIn(activeID, cookie, validate).qrcodeSignIn(enc, locationText, locationLatitude, locationLongitude)
    return parseSignIn(result)

@app.post("/signcodeSignIn")
def signcodeSignIn(
    username: str = Body(...), 
    activeID: str = Body(...),
    signCode: str = Body(...),
    validate: Optional[str] = Body(""),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = SignIn(activeID, cookie, validate).signcodeSignIn(signCode)
    return parseSignIn(result)

@app.post("/getQuizProblem")
def getQuizProblem(
    username: str = Body(...), 
    activeID: str = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = Quiz(cookie, activeID).getQuizProblem()
    return parseQuizProblem(result)

@app.post("/submitQuizProblem")
def submitQuizProblem(
    username: str = Body(...), 
    courseID: str = Body(...), 
    classID: str = Body(...), 
    activeID: str = Body(...),
    data: list = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = Quiz(cookie, activeID).submitQuizProblem(courseID, classID, data)
    return parseSubmitResult(result)

@app.post("/getDiscussion")
def getDiscussion(
    username: str = Body(...), 
    activeID: str = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = Discussion(cookie).getDiscussion(activeID)
    return parseDiscussion(result)

@app.post("/getReply")
def getReply(
    username: str = Body(...), 
    uuid: str = Body(...), 
    bbsid: str = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = Discussion(cookie).getReply(uuid, bbsid)
    return parseReply(result)

@app.post("/submitReply")
def submitReply(
    username: str = Body(...), 
    courseID: str = Body(...),
    classID: str = Body(...),
    uuid: str = Body(...), 
    bbsid: str = Body(...),
    content: str = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = Discussion(cookie).submitReply(uuid, courseID, classID, content, bbsid)
    return parseReplyResponse(result)

if __name__ == "__main__":
    uvicorn.run(app, host = listenIP, port = listenPort)
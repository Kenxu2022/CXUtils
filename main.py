from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import uvicorn
from pydantic import BaseModel
from typing import Annotated
from configparser import ConfigParser

from credentials.cookie import initializeCookie, getCookie, deleteCookie
from auth import createToken,validateToken
from api import ChaoxingAPI, SignIn
from utils.parse import parseCourse, parseActivity, parseSignInDetail, parseSignIn

class Token(BaseModel):
    access_token: str
    token_type: str

conf = ConfigParser()
conf.read('config.ini')
listenIP = conf['API']['ListenIP']
listenPort = int(conf['API']['Port'])
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
def addCredential(username: str = Body(...), password: str = Body(...), _ = Depends(getUser)):
    result = initializeCookie(username, password, False)
    result.pop('cookie')
    return result

@app.post("/deleteCredential")
def deleteCredential(username: str = Body(..., embed=True), _ = Depends(getUser)):
    result = deleteCookie(username)
    return result

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
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = ChaoxingAPI(cookie).getActivity(courseID, classID)
    return parseActivity(result)

@app.post("/getSignInDetail")
def getSignInDetail(
    username: str = Body(...), 
    activeID: str = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = SignIn(activeID, cookie).getMiscInfo()
    return parseSignInDetail(result)

@app.post("/normalSignIn")
def normalSignIn(
    username: str = Body(...), 
    activeID: str = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = SignIn(activeID, cookie).normalSignIn()
    return parseSignIn(result)

@app.post("/locationSignIn")
def locationSignIn(
    username: str = Body(...), 
    activeID: str = Body(...),
    locationText: str = Body(...),
    locationLatitude: str = Body(...),
    locationLongitude: str = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = SignIn(activeID, cookie).locationSignIn(locationText, locationLatitude, locationLongitude)
    return parseSignIn(result)

@app.post("/qrcodeSignIn")
def qrcodeSignIn(
    username: str = Body(...), 
    activeID: str = Body(...),
    enc: str = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = SignIn(activeID, cookie).qrcodeSignIn(enc)
    return parseSignIn(result)

@app.post("/signcodeSignIn")
def signcodeSignIn(
    username: str = Body(...), 
    activeID: str = Body(...),
    signCode: str = Body(...),
    _ = Depends(getUser)
):
    cookie = getCookie(username).get("cookie")
    result = SignIn(activeID, cookie).signcodeSignIn(signCode)
    return parseSignIn(result)

if __name__ == "__main__":
    uvicorn.run(app, host = listenIP, port = listenPort)
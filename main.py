from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import uvicorn
from pydantic import BaseModel
from typing import Annotated
from configparser import ConfigParser

from credentials.cookie import initializeCookie, deleteCookie
from auth import createToken,validateToken

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
    if not validateToken(token):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

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

if __name__ == "__main__":
    uvicorn.run(app, host=listenIP, port=listenPort)
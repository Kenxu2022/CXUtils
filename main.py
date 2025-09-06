from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
from typing import Annotated
from configparser import ConfigParser

from utils.cookie import initializeCookie

conf = ConfigParser()
conf.read('config.ini')
listenIP = conf['API']['ListenIP']
listenPort = int(conf['API']['Port'])
app = FastAPI(docs_url=None, redoc_url=None)

@app.post("/addCredential")
def addCredential(credential: Annotated[OAuth2PasswordRequestForm, Depends()]):
    result = initializeCookie(credential.username, credential.password, False)
    result.pop('cookie')
    return result

if __name__ == "__main__":
    uvicorn.run(app, host=listenIP, port=listenPort)
from configparser import ConfigParser
import jwt
import os
# from jwt.exceptions import InvalidTokenError
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from loguru import logger

SECERT_KEY = os.getenv("SECERT_KEY", str(uuid4()))
ALGORITHM = "HS256"

conf = ConfigParser()
conf.read('config.ini')
username = os.getenv("USERNAME", conf['Auth']['Username'])
password = os.getenv("PASSWORD", conf['Auth']['Password'])

def createToken(usernameFromClient: str, passwordFromClient: str):
    if (usernameFromClient == username and passwordFromClient == password):
        data = {
            "sub": username,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=60)
            }
        logger.info("成功签发Token")
        encodedJwt = jwt.encode(data, SECERT_KEY, algorithm = ALGORITHM)
        return encodedJwt
    else:
        logger.warning("登录用户名或密码错误，请检查与config.ini中是否一致")
        return None
    
def validateToken(token: str):
    try:
        payload = jwt.decode(token, SECERT_KEY, algorithms = ALGORITHM)
        usernameFromToken = payload.get("sub")
        if usernameFromToken == username:
            return username
        else:
            logger.error("无法验证Token，用户不存在")
            return None
    except:
        logger.error("无法验证Token")
        return None
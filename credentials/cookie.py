import requests
import json
from loguru import logger
from datetime import datetime

from credentials.encrypt import loginEncrypt
from credentials.db import DatabaseManager

LOGIN_HEADER = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.8,zh-TW;q=0.6,ja;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'retain-login=1', # 1: auto login 2: not auto login
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }
LOGIN_URL = "https://passport2.chaoxing.com/fanyalogin"


def initializeCookie(username: str, password: str, isPasswordEncrypted: bool):
    password = password if isPasswordEncrypted else loginEncrypt(password)
    data = {
        'fid': -1,
        'uname': loginEncrypt(username),
        'password': password,
        't': 'true' # mandatory
    }
    response = requests.post(LOGIN_URL, headers = LOGIN_HEADER, data = data)
    status = json.loads(response.text).get('status')
    if not status:
        detail = json.loads(response.text).get('msg2')
        logger.error("登录失败，请检查账号密码是否正确")
        return {
            'success': False,
            'cookie': None,
            'detail': detail if detail else "未知错误"
        }
    else:
        logger.info("登录成功！")
        cookie = response.cookies
        with DatabaseManager() as dbManager:
            dbManager.addCookie(username, password, cookie)
        return {
            'success': True,
            'cookie': cookie,
            'detail': None
        }

def getCookie(username: str):
    with DatabaseManager() as dbManager:
        result = dbManager.getCookie(username)
    currentTime = round(datetime.now().timestamp())
    if currentTime - result['addTime'] < 604800: # within 7 days
        logger.info("成功获取Cookie")
        return {
            'success': True,
            'cookie': result['cookie'],
            'detail': None
        }
    else:
        logger.info("Cookie添加超过7天，刷新中")
        encpassword = result['encpassword']
        return initializeCookie(username, encpassword, True)
    
def deleteCookie(username: str):
    with DatabaseManager() as dbManager:
        dbManager.deleteCookie(username)
    return {
        "success": True,
        "detail": None
    }
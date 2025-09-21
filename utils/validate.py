from loguru import logger
from ddddocr import DdddOcr
from requests.cookies import RequestsCookieJar
import time

from api import Captcha
from utils.parse import parseServerTime, parseCaptchaImageUrl, parseValidateCode
from utils.captcha import getCaptchaParam, getCoordinate

parseCaptcha = DdddOcr(show_ad=False, det=False, ocr=False)

def generateValidateCode(cookie: RequestsCookieJar, courseID: str, classID: str, activeID: str):
    captchaInstance = Captcha(cookie, courseID, classID, activeID)
    for i in range(4):
        # get server time
        serverTime = parseServerTime(captchaInstance.getServerTime())
        # get current time
        timestamp = int(time.time() * 1000)
        # get parameters to obtain captcha picture
        captchaKey, token, iv = getCaptchaParam(serverTime, timestamp)
        # get captcha token and picture
        captchaToken, slideImage, backgroundImage = parseCaptchaImageUrl(captchaInstance.getCaptcha(captchaKey, token, iv, timestamp))
        # get x coordinate
        xCoordinate = getCoordinate(parseCaptcha, captchaInstance.getImage(slideImage), captchaInstance.getImage(backgroundImage))
        time.sleep(0.5)
        # get validation code
        validateCode = parseValidateCode(captchaInstance.getAuth(captchaToken, xCoordinate, iv, timestamp))
        if validateCode:
            logger.info("通过验证码校验")
            return validateCode
        logger.warning(f"未通过验证码校验，次数：第{i + 1}次")
    logger.error("连续五次失败，终止")
    return {
        "success":False,
        "code": None
    }
# captchaKey = MD5加密(服务器返回时间 + 随机UUID)
# token = MD5加密(服务器返回时间 + captchaId + 'slide' + captchaKey) + ':' + ttl
# iv = MD5加密(captchaId + 'slide' + 当前时间 + 随机UUID)
# ttl = 服务器返回时间 + 300000ms

from uuid import uuid1
from hashlib import md5
from ddddocr import DdddOcr

CAPTCHA_ID = "Qt9FIw9o4pwRjOyqM6yizZBh682qN2TU"

def getCaptchaParam(server_time, timestamp):
    captchaKey = md5((f"{server_time}{uuid1}").encode("utf-8")).hexdigest()
    token = md5((f"{server_time}{CAPTCHA_ID}slide{captchaKey}").encode("utf-8")).hexdigest() + ":" + f"{server_time + 300000}"
    iv = md5((f"{CAPTCHA_ID}slide{timestamp}{uuid1}").encode('utf-8')).hexdigest()
    return captchaKey, token, iv

def getCoordinate(slideImage: bytes, backgroundImage: bytes):
    parseCaptcha = DdddOcr(show_ad=False, det=False, ocr=False)
    coordinate = parseCaptcha.slide_match(slideImage, backgroundImage, simple_target=True)

    x_end = coordinate['target'][2]
    # slide distance is from -8 to 272
    x_coordinate = x_end - 56 + 8
    return x_coordinate

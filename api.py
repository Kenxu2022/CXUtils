import requests
import json

HEADER = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.8,zh-TW;q=0.6,ja;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

class ChaoxingAPI:
    def __init__(self, cookie):
        self.cookie = cookie
    def getCourse(self):
        url = "https://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1"
        response = requests.get(url, headers = HEADER, cookies=self.cookie)
        return json.loads(response.text)
    def getActivity(self, courseId: str, classId: str):
        url = "https://mobilelearn.chaoxing.com/v2/apis/active/student/activelist"
        data = {
            'fid': 0,
            'courseId': courseId,
            'classId': classId
        }
        response = requests.get(url, headers = HEADER, params = data, cookies = self.cookie)
        return json.loads(response.text)
    
class SignIn:
    def __init__(self, activeId, cookie, validate = ""):
        self.activeId = activeId
        self.cookie = cookie
        self.validate = validate
    def normalSignIn(self):
        url = f"https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId={self.activeId}&validate={self.validate}"
        response = requests.get(url, headers = HEADER, cookies = self.cookie)
        return response.text
    def locationSignIn(self, locationText, locationLatitude, locationLongitude):
        url = f"https://mobilelearn.chaoxing.com/pptSign/stuSignajax?address={locationText}&activeId={self.activeId}&latitude={locationLatitude}&longitude={locationLongitude}&validate={self.validate}&fid=0&appType=15&ifTiJiao=1"
        response = requests.get(url, headers = HEADER, cookies = self.cookie)
        return response.text
    def qrcodeSignIn(self, enc):
        url = f"https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId={self.activeId}&enc={enc}&validate={self.validate}&fid=0"
        response = requests.get(url, headers = HEADER, cookies = self.cookie)
        return response.text
    def signcodeSignIn(self, signcode):
        url = f"https://mobilelearn.chaoxing.com/v2/apis/sign/signIn?activeId={self.activeId}&signCode={signcode}&validate={self.validate}&moreClassAttendEnc="
        response = requests.get(url, headers = HEADER, cookies = self.cookie)
        return response.text
    def getMiscInfo(self):
        url = f"https://mobilelearn.chaoxing.com/v2/apis/active/getPPTActiveInfo?activeId={self.activeId}"
        response = requests.get(url, headers = HEADER, cookies = self.cookie)
        return json.loads(response.text)
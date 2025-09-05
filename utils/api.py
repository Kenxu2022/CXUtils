import requests
import json
import re
from uuid import uuid4
from urllib.parse import quote

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
    def getQuestion(self, activeId: str):
        url = "https://mobilelearn.chaoxing.com/v2/apis/discuss/getTopicDiscussInfo"
        data = {
            'activeId': activeId
        }
        response = requests.get(url, headers = HEADER, params = data, cookies = self.cookie)
        responseData = response.json()
        questionUUID = responseData['data']['uuid']
        url = f"https://groupweb.chaoxing.com/course/topicDiscuss/{questionUUID}/getTopic"
        response = requests.get(url, headers = HEADER, cookies = self.cookie)
        responseData = response.json()
        question = responseData['datas']['text_content']
        publicURL = responseData['datas']['shareUrl']
        uuid = responseData['datas']['uuid']
        bbsid = responseData['datas']['bbsid']
        return question, publicURL, uuid, bbsid
    def getReply(self, uuid: str, bbsid: str):
        url = f"https://sharewh1.xuexi365.com/share/topic/{bbsid}/{uuid}/replys.json"
        response = requests.get(url, headers = HEADER, cookies = self.cookie)
        return response.json()
    def _getURLToken(self, uuid: str):
        url = "https://groupweb.chaoxing.com/course/topicDiscuss/info"
        data = {
            'uuid': uuid
        }
        response = requests.get(url, headers = HEADER, params = data, cookies = self.cookie)
        htmlContent = response.text
        pattern = r"urlToken:'([^']+)'"
        urlToken = re.search(pattern, htmlContent).group(1)
        return urlToken
    def sendReply(self, uuid: str, courseId: str, classId: str, content: str, bbsid: str):
        url = f"https://groupweb.chaoxing.com/pc/invitation/{uuid}/addReplys"
        data = {
            'courseId': courseId,
            'classId': classId,
            'replyId': -1,
            'uuid': uuid4(),
            'topic_content': quote(content),
            'urlToken': self._getURLToken(uuid),
            'bbsid': bbsid,
            'anonymous': ""
        }
        response = requests.post(url, headers = HEADER, data = data, cookies = self.cookie)
        return response.json()
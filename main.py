import  WeibanAPI
import time
import webbrowser
from rich.console import Console
from rich.console import Console
console = Console()
def run():

    console.print('{:=^45}'.format('安全微课逃课助手v3.0'))
    console.print("程序仅供学习，不得用作商业用途")
    console.print('多学一些安全知识也不是没有用\n')
    console.print('考试功能未做，可以看GitHub上面的更新时间')
    console.print("1.5s后自动打开浏览器，需要你 [bold cyan]手动登录 [bold cyan]安全微课")
    console.print('2.使用学号 [bold cyan]登录 [bold cyan]， [bold red]密码默认是学号后六位 [bold red]')
    console.print("3.登录以后输入按F12或打开检查，在控制台输入这条命令")
    console.print("如果卡住请按一下ctrl+c",style="red on white")

    console.print('''data=JSON.parse(localStorage.user);prompt('',data['token']+"&"+data['userId']+"&"+data['tenantCode'])''')
    with console.status("[bold green]正在打浏览器...") as status:
            time.sleep(5)
    webbrowser.open("https://weiban.mycourse.cn/#/")
    info=input("把刚刚浏览器获取到的信息复制进来并按下回车：\n")

    info=info.split('&')
    print(info[0],info[1],info[2])
    data = {"token": info[0], "userId": info[1],
            "tenantCode": info[2]}
    userId = data['userId']
    # print(wb.userId)
    token = data['token']
    # # print(wb.token)
    tenantCode = data['tenantCode']
    wb = WeibanAPI.WeibanAPI(token=token,userId=userId,tenantCode=tenantCode)
    # next_step = input("下一步:\n")
    # if next_step == 'n':

    print("获取学生信息")
    wb.getInfo()
    print('获取学生任务')
    # wait_time = wb.getRandomtime()
    # print('等待{}秒'.format(wait_time))
    # time.sleep(wait_time)
    wb.getTask()
    wb.getProgress()
    print('获取课程列表')
    wb.getCourse()
    wb.finshiall()
    print("全部刷完了")
if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print("再见~~")
        time.sleep(5)
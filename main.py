import  WeibanAPI
import time
import webbrowser
from rich.console import Console
from rich.console import Console
console = Console()

def run():

    console.print('{:=^45}'.format('安全微课逃课助手v3.2'))
    console.print("程序仅供学习，完全免费")
    console.print('多学一些安全知识也不是没有用\n')
    console.print('考试功能已做',style="red on white")
    console.print("1.5s后自动打开浏览器，需要你 [bold cyan]手动登录 [bold cyan]安全微课")
    console.print('2.使用学号 [bold cyan]登录 [bold cyan]， [bold red]密码默认是学号后六位 [bold red]')
    console.print("3.登录以后输入按F12或打开检查，在控制台输入这条命令")
    console.print("如果卡住请按一下ctrl+c",style="red on white")

    console.print('''data=JSON.parse(localStorage.user);prompt('',data['token']+"&"+data['userId']+"&"+data['tenantCode'])''')
    with console.status("[bold green]正在打浏览器...") as status:
            time.sleep(3)
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
    print("获取学生信息")
    wb.getInfo()
    print('获取学生任务')
    wb.getTask()
    wb.getProgress()
    print('获取课程列表')
    wb.getCourse()
    wb.finshiall()
    print("全部刷完了")
    console.log("[bold cyan]开始考试[bold cyan]")
    console.log("不敢保证百分百可以过考试",style="red on white")
    count=0
    flag=False
    while  flag == False:
        flag=check(wb)
        print(flag)

    while count<2:
        count += 1
        console.log(f"第{count}次尝试")

        try:
            res=wb.do_paper()
        except Exception as e:
            print("没有刷完题，请重新运行补刷",e)
            input()

        # print(res)
        wb.get_ques()
        res=res['data']['score']
        if res>=90:
            console.log(f"本次分数为：[bold green]{res}[bold green]")
            console.log(f"成绩合格")
            break
        else:
            console.log(f"本次分数为：[bold red]{res}[bold red]")
            console.log(f"成绩不合格")

def check(wb):
    flag=wb.getProgress()
    print("未刷完，检查重刷")
    wb.getInfo()
    wb.getTask()
    wb.getProgress()
    wb.getCourse()
    wb.finshiall()
    print(flag)
    return flag

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print("再见~~")
        time.sleep(5)
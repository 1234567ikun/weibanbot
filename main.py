import  WeibanAPI
import time
import webbrowser
def run():
    wb = WeibanAPI.WeibanAPI()
    a = wb.qrLogin()
    print('{:=^45}'.format('安全微课逃课助手'))
    print("程序仅供学习，不得用作商业用途")
    print('多学一些安全知识也不是没有用\n')
    print("5s后跳出来的链接用微信扫描，登录完成之后输入小写‘n’开始")
    time.sleep(6)
    print('登录连接:', a)
    webbrowser.open(a)
    next_step = input("下一步:\n")
    if next_step == 'n':
        wb.freashLogin()
        print("获取学生信息")
        wb.getInfo()
        print('获取学生任务')
        wait_time = wb.getRandomtime()
        print('等待{}秒'.format(wait_time))
        time.sleep(wait_time)
        wb.getTask()
        wb.getProgress()
        print('获取课程列表')
        wb.getCourse()
        wb.finshiall()
        print("全部刷完了")
if __name__ == '__main__':
    run()
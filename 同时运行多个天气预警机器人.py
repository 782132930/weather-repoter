import os
import threading

def get_argss():
    argss=[]
    try:
        fo = open('用户信息.txt', 'r',encoding='gb2312')  # 打开用户信息文件
        user_message = fo.read()
        user_message = eval(user_message)
        for message in user_message:
            args='下雨预警（酷Q）脚本2.0.py'+' '+message['location'] +' '+message['qq']#linux在python3环境下运行并前面加上python
            argss.append(args)
        fo.close()
        return argss
    except:
        print("API文件打开失败，请检查原因")

def run_codes(args):
    os.system(args)#命令行运行.py文件

if __name__ == '__main__':
    argss=get_argss()
    threads=[]
    #多线程执行多个程序
    for args in argss:
        t = threading.Thread(target=run_codes,args=(args,))
        threads.append(t)
    for t in threads:
        t.start()#启动线程
    for t in threads:
        t.join() #线程等待结束

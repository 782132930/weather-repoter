# 导入相应的包
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def post_qqemail():
    # MIMEText三个主要参数
    # 1. 邮件内容
    # 2. MIME子类型，在此案例我们用plain表示text类型
    # 3. 邮件编码格式，一定要用"utf-8"编码，因为内容可能包含非英文字符，不用的可能收到的邮件是乱码
    msg = MIMEText("预警内容", "plain", "utf-8")
    # 填写发送方的信息
    header_from = Header("小明", "utf-8")
    msg['From'] = header_from

    # 填写接受方的信息
    header_to = Header("小红", 'utf-8')
    msg['To'] = header_to

    # 填写该邮件的主题
    header_sub = Header("这里填写主题", 'utf-8')
    msg['Subject'] = header_sub

    # 发送email地址，填入你授权码的那个邮箱地址，此处地址是我常用QQ的地址
    from_addr = "782132930@qq.com"
    # 此处密码填你之前获得的授权码，不是你的QQ邮箱密码
    from_pwd = "mkppfjzohsXXXX"

    # 接受email地址，填入你要发送的邮箱地址，此处地址是我另外一个QQ小号的邮箱地址
    to_addr = "782132930@qq.com"

    # 输入SMTP服务器地址，并使用该服务器给你发送电子邮件
    # 此处根据不同的邮件服务商有不同的值，
    # 现在基本任何一家邮件服务商，如果采用第三方收发邮件，都需要开启授权选项
    # 腾讯QQ邮箱的SMTP地址是"smtp.qq.com"
    smtp_srv = "smtp.qq.com"

    try:
        # 不能直接使用smtplib.SMTP来实例化，第三方邮箱会认为它是不安全的而报错
        # 使用加密过的SMTP_SSL来实例化，它负责让服务器做出具体操作，它有两个参数
        # 第一个是服务器地址，但它是bytes格式，所以需要编码
        # 第二个参数是服务器的接受访问端口，SMTP_SSL协议默认端口是465
        srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465)
        # 使用授权码登录你的QQ邮箱
        srv.login(from_addr, from_pwd)
        # 使用sendmail方法来发送邮件，它有三个参数
        # 第一个是发送地址
        # 第二个是接受地址，是list格式，意在同时发送给多个邮箱
        # 第三个是发送内容，作为字符串发送
        srv.sendmail(from_addr, [to_addr], msg.as_string())
        print('发送成功')
    except Exception as e:
        print('发送失败')
    finally:
        #无论发送成功还是失败都要退出你的QQ邮箱
        srv.quit()
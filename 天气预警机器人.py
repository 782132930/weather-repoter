import requests
import time
import json
import sys
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback

flag=0
#定义字典：
weather_describe={'CLEAR_DAY':'晴（白天）','CLEAR_NIGHT':'晴（夜间）','PARTLY_CLOUDY_DAY':'多云（白天）','PARTLY_CLOUDY_NIGHT':'多云（夜间）','CLOUDY':'阴','WIND':'大风','HAZE':'雾霾','RAIN':'雨','SNOW':'雪'}

def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status() #如果状态不是200，引发异常
        #r.encoding = 'utf - 8' #无论原来是什么编码，全部改用utf-8
        return r.text
    except:
        return ""

def compose_url(longitude,latitude,model):#0:天级，1:时级，2:分钟级别
    if model == 2:
        url='https://api.caiyunapp.com/v2/JWzcF9SoXXXXX/'+longitude+','+latitude+'/minutely?&getplacename=True'
    #url ='https://api.caiyunapp.com/v2/JWzcF9SoeXXXXX/113.381699,23.046000/minutely?&getplacename=True'
    elif model == 0:
        url = 'https://api.caiyunapp.com/v2/JWzcF9SoeXXXX/' + longitude + ',' + latitude + '/daily?&getplacename=True&dailysteps=1&unit=metric:v1'
    return url

def list_str(list):
    list_str=[str(i) for i in list]
    string = ",".join(list_str)
    return string

def keep_decimal(list,num):
    list_keep=[]
    for data in list:
        list_keep.append(round(data, num))
    return list_keep

def sunny_tip(html):
    # global count
    # global count1
    weather_prediction = json.loads(html)
    #weather_prediction = eval(html)
    if weather_prediction['status'] =='ok':
        minutely=weather_prediction['result']["minutely"] #分钟预报内容
        placename=weather_prediction["placename"] #地理位置
        location=[str(i) for i in weather_prediction["location"] ] #经纬度
        location=list_str(location)
        if minutely[ 'probability'][0] == 0:
            description  =minutely['description'] #天气状况描述
            probability = minutely["probability"] #两小时下雨概率
            probability=keep_decimal(probability,2)
            probability = list_str(probability)
            #probability_4h = minutely["probability_4h"]#4小时下雨概率
            #probability_4h=keep_decimal(probability_4h,2)
            #probability_4h = list_str(probability_4h)
            warning='地理位置：' + placename + '\n' \
                    +'下雨预警：'+description+'\n' \
                    +'未来2小时，逐半小时，雷达降水概率预报：'+'\n' \
                    + probability +'\n'
                    #+'天气状况：'+description +'\n' \
            return warning
        # for result in weather_prediction['result']["minutely"]:
        #     a=weather_prediction['result']["minutely"].get(result)
        #     print(a)
    else:
        print("查询彩云天气服务器失败")

def rain_alerting(html):
    # global count
    # global count1
    weather_prediction = json.loads(html)
    #weather_prediction = eval(html)
    if weather_prediction['status'] =='ok':
        minutely=weather_prediction['result']["minutely"] #分钟预报内容
        placename=weather_prediction["placename"] #地理位置
        location=[str(i) for i in weather_prediction["location"] ] #经纬度
        location=list_str(location)
        if minutely[ 'probability'][0] > 0.1:
            description  =minutely['description'] #天气状况描述
            probability = minutely["probability"] #两小时下雨概率
            probability=keep_decimal(probability,2)
            probability = list_str(probability)
            #probability_4h = minutely["probability_4h"]#4小时下雨概率
            #probability_4h=keep_decimal(probability_4h,2)
            #probability_4h = list_str(probability_4h)
            warning='地理位置：' + placename + '\n' \
                    +'下雨预警：'+description+'\n' \
                    +'未来2小时，逐半小时，雷达降水概率预报：'+'\n' \
                    + probability +'\n'
                    #+'天气状况：'+description +'\n' \
            return warning
        # for result in weather_prediction['result']["minutely"]:
        #     a=weather_prediction['result']["minutely"].get(result)
        #     print(a)
    else:
        print("查询彩云天气服务器失败")

def post_qqnews(text,qqs):
    #http://127.0.0.1:5700/send_private_msg?user_id=123456&message=你好
    urls=[]
    for qq in qqs:
        string='http://127.0.0.1:5700/send_private_msg?user_id='+qq+'&message='+text
        urls.append(string)
    for url in urls:
        getHTMLText(url)

def post_stop_qqemail():
    # MIMEText三个主要参数
    # 1. 邮件内容
    # 2. MIME子类型，在此案例我们用plain表示text类型
    # 3. 邮件编码格式，一定要用"utf-8"编码，因为内容可能包含非英文字符，不用的可能收到的邮件是乱码
    msg = MIMEText("天气监测系统出现故障！", "plain", "utf-8")
    # 填写发送方的信息
    header_from = Header("高倾健", "utf-8")
    msg['From'] = header_from

    # 填写接受方的信息
    header_to = Header("自己", 'utf-8')
    msg['To'] = header_to

    # 填写该邮件的主题
    header_sub = Header("服务器运行监视", 'utf-8')
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

#########################################################
def judge_wind_direction(wind_direction):
    if wind_direction>=0:
        wind_direction_str='东北风'
        if wind_direction>=90:
            wind_direction_str='东南风'
            if wind_direction>=180:
                wind_direction_str='西南风'
                if wind_direction>=270:
                    wind_direction_str='西北风'
    return wind_direction_str

def judge_wind_level(win_speed_max):
    if win_speed_max>=0:
        wind_level_str='0级-无风'
        if win_speed_max>=0.3:
            wind_level_str='1级-软风'
            if win_speed_max>=1.6:
                wind_level_str='2级-轻风'
                if win_speed_max >=3.4:
                    wind_level_str = '3级-微风'
                    if win_speed_max >=5.5:
                        wind_level_str = '4级-和风'
                        if win_speed_max >=8:
                            wind_level_str = '5级-轻劲风'
                            if win_speed_max >=10.8:
                                wind_level_str = '6级-强风'
                                if win_speed_max >=13.9:
                                    wind_level_str = '7级-疾风'
                                    if win_speed_max >=17.2:
                                        wind_level_str = '8级-大风'
                                        if win_speed_max >=20.8:
                                            wind_level_str = '9级-烈风'
                                            if win_speed_max >=24.5:
                                                wind_level_str = '10级-狂风'
                                                if win_speed_max >=28.5:
                                                    wind_level_str = '11级-暴风'
                                                    if win_speed_max >=32.7:
                                                        wind_level_str = '12级-台风'
                                                        if win_speed_max >=37:
                                                            wind_level_str = '13级以上台风'
    return wind_level_str

def judge_rain_level(precipitation_max):
    if precipitation_max > 0.03:
        precipitation_str = '有小雨（雪）'
        if precipitation_max > 0.25:
            precipitation_str = '有中雨（雪）'
            if precipitation_max > 0.35:
                precipitation_str = '有大雨（雪）'
                if precipitation_max > 0.48:
                    precipitation_str = '有暴雨（雪）'
    else:
        precipitation_str = '无雨'
    return precipitation_str

def judge_aqi(aqi_avg):
    if aqi_avg>=0:
        aqi_str='优'
        if aqi_avg >= 50:
            aqi_str = '良好'
            if aqi_avg >= 100:
                aqi_str = '轻度污染'
                if aqi_avg >= 150:
                    aqi_str = '中度污染'
                    if aqi_avg >=200:
                        aqi_str = '重度污染'
                        if aqi_avg >=300:
                            aqi_str = '严重污染'
    return aqi_str

def weather_prediction(html):
    weather_prediction = json.loads(html)
    if weather_prediction['status'] == 'ok':
        daily = weather_prediction['result']["daily"]  # 天级别预报内容
        placename = weather_prediction["placename"]  # 地理位置
        location = [str(i) for i in weather_prediction["location"]]  # 经纬度
        location = list_str(location)
        skycon =  daily['skycon'][0]["value"]# 全天天气状况
        skycon_20h_32h = daily['skycon_20h_32h'][0]["value"]  # 夜间天气状况
        skycon_08h_20h = daily['skycon_08h_20h'][0]["value"]  # 白天天气状况
        skycon,skycon_20h_32h,skycon_08h_20h = weather_describe[skycon],weather_describe[skycon_20h_32h],weather_describe[skycon_08h_20h]  # 更新为中文

        temperature = daily['temperature'][0] # 温度
        cloudrate = daily['cloudrate'][0] # 相对云量
        dswrf = daily['dswrf'][0]  # 短波辐射
        aqi = daily['aqi'][0]  # aqi指数
        aqi_avg=aqi['avg']
        visibility = daily['visibility'][0]#能见度
        humidity = daily['humidity'][0]#湿度
        pres =daily['pres'][0]#气压
        pm25 = daily['pm25'][0] #pm25
        precipitation = daily['precipitation'][0] #降雨量

        aqi_avg=judge_aqi(aqi_avg)
        astro = daily['astro']  # 日出日落时间
        sunset = astro[0]['sunset']['time']#日落时间
        sunrise = astro[0]['sunrise']['time']  # 日出时间

        wind=daily['wind'][0]#风力计算
        wind_direction=wind['avg']['direction']#平均风向
        wind_speed_max=round(wind['max']['speed']/3.6,2)#平均风速 单位：m/s 保留两位小数
        wind_direction=judge_wind_direction(wind_direction)#转换成文字描述风向
        wind_speed_max=judge_wind_level(wind_speed_max)#转换成文字描述风速

        comfort = daily['comfort'][0]["desc"]  # 舒适度描述
        coldRisk = daily['coldRisk'][0]["desc"]  # 感冒度描述
        ultraviolet = daily['ultraviolet'][0]["desc"]  # 紫外线强度描述
        carWashing =  daily['carWashing'][0]["desc"]  # 洗车描述

        precipitation_max = judge_rain_level(precipitation['max'])


        prediction =  temperature['date']+'天气预报:'  + '\n' \
                  + '地理位置：' + placename + '\n' \
                      + '白天主要天气现象：' + skycon_08h_20h + '\n' \
                      + '夜晚主要天气现象：' + skycon_20h_32h + '\n' \
                      + '紫外线指数：' + ultraviolet + '\n' \
                      + '舒适度指数：' + comfort + '\n' \
                      + '洗车指数：' + carWashing + '\n' \
                      + '感冒指数：' + coldRisk + '\n' \
                      + '日出日落：' + sunrise + ' | ' + sunset + '\n'\
                  + '温度：' + str(temperature['min']) + '~' + str(temperature['max']) + '\n' \
                  + '相对湿度（%）：' +str(humidity['min']) +'~'+str(humidity['max']) + '\n' \
                  + '降水强度：' +precipitation_max + '\n' \
                  + '风力等级（max）：'+wind_speed_max+ '\n' \
                  + '风向：'+wind_direction+'\n' \
                  + 'PM25浓度：' +str(pm25['min']) +'~'+str(pm25['max']) +'\n'\
                  + '空气质量：'+aqi_avg+'\n'
        return prediction
    else:
        print("查询彩云天气服务器失败")

def post_daily_weather(url,qqs):
    global flag
    t = time.localtime(time.time())
    if t.tm_hour < 6 and (flag == 0):
        flag = 1
    elif t.tm_hour > 6:
        flag = 0
    if flag == 1:
        html = getHTMLText(url)
        prediction = weather_prediction(html)
        post_qqnews(prediction,qqs)
        print(prediction)
        flag=2

if __name__ == '__main__':
    try:
        action = random.uniform(0, 120)
        print(action)
        print('天气监测系统运行正常')
        time.sleep(60*action)
        print('天气监测系统运行正常')
        longitude,latitude = sys.argv[1].split(',')
        #longitude,latitude='113.386394','23.043321'
        url_warn=compose_url(longitude,latitude,2)
        url_pre = compose_url(longitude,latitude,0)
        user_qqs=[]
        user_qqs=sys.argv[2].split(',')
        #user_qqs.append('782132930')
        flag=0
        weather_flag=0 #根据天气情况自己调节
        while(1):
            count = random.uniform(15, 30)
            html=getHTMLText(url_warn)
            warning=rain_alerting(html)
            post_daily_weather(url_pre,user_qqs)
            if warning is None:
                if weather_flag == 1:
                    count1 = random.uniform(5, 10)
                    time.sleep(count1 * 60)
                    html = getHTMLText(url_warn)
                    tips = sunny_tip(html)
                    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    if tips is None:
                        print('{}目前没有晴天提醒'.format(t))
                    else:
                        tips = sunny_tip(html)
                        post_qqnews(tips, user_qqs)
                        print('{}已发送晴天提醒'.format(t))
                        print(tips)
                        weather_flag = 0

            else:
                if weather_flag == 0:
                    count2=random.uniform(5,10)
                    time.sleep(count2*60)
                    html = getHTMLText(url_warn)
                    warning = rain_alerting(html)
                    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    if warning is None:
                        print('{}目前没有下雨预警'.format(t))
                    else:
                        post_qqnews(warning, user_qqs)
                        print('{}已发送下雨预警'.format(t))
                        print(warning)
                        weather_flag = 1
            time.sleep(60*count)
    except:
        print('天气监测系统出现故障！')
        post_stop_qqemail()
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(t)
        traceback.print_exc()  # 返回字符串
        traceback.format_exc()  # 直接给打印出来
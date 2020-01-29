天气预警机器人  
使用前提：  
1）天气预警机器人.py中的彩云天气密匙需要自己去注册获取，邮箱授权码也需要自己去获取，然后填写好。  
2）程序中的酷Q需要一直挂着，并且安装和启动了http-API插件。  
3）酷Q登录的小号必须提前加好接受天气信息的用户。  
4）程序还有用户信息.txt需要放在同一个文件夹或目录下。  
5）用户信息的编写参考用户信息.txt（包括经纬度和QQ号）。  
6）.zip压缩包解压即可使用酷Q。  

程序使用方法是：  
1）编辑好用户信息，然后一直挂着酷Q，直接运行“同时运行多个天气预警机器人.py”即可。  
2）为了避免酷Q被冻结而不知，还写了一个酷Q检测程序，通过QQ邮箱发送，也需要授权码，直接运行即可。  

程序功能说明：  
1）天气预警机器人可对多个地点的多个用户以及同一地点的多个用户进行服务。  
2）每日的24：00后机器人会自动对每个QQ用户发送第二天的天气状况。  
3）实时地监测记事本中的经纬度地点的天气状况，当发现下雨概率比较大的时候推送下雨预警，当快停雨了就推送停雨提醒。  
4）由于酷Q本身自带的聊天功能，所以推送天气信息的小号同时也能实现自动聊天功能。  

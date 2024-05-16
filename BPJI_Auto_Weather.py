#!/usr/bin/env python3
"""
脚本名称：Pager weather forecast
脚本地址: https://github.com/bg8ixz/Pager_weather_forecast
脚本版本: 1.0.3
更新内容：* 增加多ID发送天气预报以及次日天气预报； * 增加发送随机时长间隔，保护发射机；
"""
import os
import requests
from datetime import datetime
import urllib.parse as up
import time
import json
import pytz
import random

today_date = datetime.today().strftime("%Y年%m月%d日")
taskno = int(time.time() * 1000)  # 获取当前时间的时间戳

# 从配置的CALL_NUMBER获取BB机ID号列表
call_number_raw = os.environ['CALL_NUMBER']
call_numbers = [call for call in call_number_raw.strip().split('\n') if call]

class SendInfoManager:
    def __init__(self, index=0):
        self.index = index
        self.load_send_info()
        self.set_info()

    def load_send_info(self):
        self.send_info_json = os.environ['SEND_INFO']       # 读取配置
        self.send_info = json.loads(self.send_info_json)      # 将字符串转换列表

    def set_info(self):
        # 设置变量
        info = self.get_info_by_index(self.index)
        self.url = info.get('url')
        self.api_key = info.get('api_key')
        self.city_code = info.get('city_code')
        self.region = info.get('region')
        self.STN = info.get('STN')

    def get_info_by_index(self, index):
        # 返回SEND_INFO列表中指定索引的信息
        return self.send_info[index]

manager = SendInfoManager()
# 配置信息
url = manager.url
api_key = manager.api_key
city_code = manager.city_code
region = manager.region
STN = manager.STN

def get_weather_forecast(api_key, city_code):
    base_url = "https://devapi.qweather.com/v7/weather/3d?"     # 使用和风天气API
    complete_url = f"{base_url}location={city_code}&key={api_key}"
    response = requests.get(complete_url)
    weather_data = response.json()
    
    if weather_data["code"] == "200":
        today = weather_data["daily"][0]
        tomorrow = weather_data["daily"][1]
        # 今天的天气信息
        today_fx_date = today["fxDate"]     # 预报日期
        today_temp_max = today["tempMax"]     # 预报当天最高温度
        today_temp_min = today["tempMin"]       # 预报当天最低温度
        today_text_day = today["textDay"]     # 预报白天天气状况
        today_text_night = today["textNight"]       # 预报夜间天气状况
        today_wind_dir_day = today["windDirDay"]     # 预报白天风向
        today_wind_scale_day = today["windScaleDay"]     # 预报白天风力等级
        today_wind_speed_day = today["windSpeedDay"]     # 预报白天风速，公里/小时
        today_wind_dir_night = today["windDirNight"]        # 预报夜间当天风向
        today_wind_scale_night = today["windScaleNight"]        # 预报夜间风力等级
        today_wind_speed_night = today["windSpeedNight"]       # 预报夜间风速，公里/小时
        # 明天的天气信息
        tomorrow_fx_date = tomorrow["fxDate"]
        tomorrow_temp_max = tomorrow["tempMax"]
        tomorrow_temp_min = tomorrow["tempMin"]
        tomorrow_text_day = tomorrow["textDay"]
        tomorrow_text_night = tomorrow["textNight"]
        tomorrow_wind_dir_day = tomorrow["windDirDay"]
        tomorrow_wind_scale_day = tomorrow["windScaleDay"]
        tomorrow_wind_speed_day = tomorrow["windSpeedDay"]
        tomorrow_wind_dir_night = tomorrow["windDirNight"]
        tomorrow_wind_scale_night = tomorrow["windScaleNight"]
        tomorrow_wind_speed_night = tomorrow["windSpeedNight"]

        forecast = f"【{today_date}天气预报】{region}今天白天{today_text_day}，最高{today_temp_max}摄氏度，{today_wind_dir_day}{today_wind_scale_day}级，风速{today_wind_speed_day}公里/小时；" \
                   f"夜间{today_text_night}，最低气温{today_temp_min}摄氏度，{today_wind_dir_night}{today_wind_scale_night}级，风速{today_wind_speed_night}公里/小时；" \
                   f"明天白天{tomorrow_text_day}，最高{tomorrow_temp_max}摄氏度，{tomorrow_wind_dir_day}{tomorrow_wind_scale_day}级，风速{tomorrow_wind_speed_day}公里/小时；" \
                   f"夜间{tomorrow_text_night}，最低气温{tomorrow_temp_min}摄氏度，{tomorrow_wind_dir_night}{tomorrow_wind_scale_night}级，风速{tomorrow_wind_speed_night}公里/小时。" \
                   f"[{STN}]"

        return forecast
    else:
        return f"【{today_date}】抱歉，天气预报服务好像出了问题，请向管理员反馈！[{STN}]"

# 遍历所有BB机ID号，发送信息
for call in call_numbers:
    print(f"原始的BB机ID号: {call}")    # 控制台被隐藏，我得试试看！
    if not call:  # 确保ID不为空
        continue    
    # 获取运行时间
    system_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    # 构造请求参数
    params = {
        'taskno': int(time.time() * 1000),  # 当前时间的时间戳（GET请求需要）
        'call': call,  # BB机ID号
        'msg': get_weather_forecast(api_key, city_code)  # 获取天气信息
    }

    # 将参数编码为URL查询字符串
    query_string = up.urlencode(params)

    # 完整的请求URL
    full_url = f"{url}?{query_string}"

    # 发送GET请求开始发天气预报
    response = requests.get(full_url)

    print(f"系统时间：{system_time}\n北京时间：{beijing_time}")
    if response.text == "0":
        print(f"{call}：天气预报发送成功（{response.text}）！")
    else:
        print(f"{call}：天气预报发送失败：{response.text}！")
    print(f"提交信息：{full_url}")      # 主要为了查看终端是否发送成功

    # 等待一个延迟发送的随机时间（怕背不住）
    time.sleep(random.uniform(20, 30))

print("【温馨提醒】所有传呼台终端天气预报已发送完毕！")
#!/usr/bin/env python3
"""
脚本名称：BPJI Weather warning
脚本地址: https://github.com/bg8ixz/Pager_weather_forecast 
脚本版本: 1.0.1
更新内容：* 修复了网络请求方法；* 优化了JSON处理；* 添加了异常处理；* 格式化打印预警信息；
"""
import requests
import json
import os
import random
import time
from datetime import datetime
import urllib.parse as up
import pytz

# 从配置的CALL_NUMBER获取BB机ID号列表
call_number_raw = os.environ['CALL_NUMBER']
call_numbers = [call for call in call_number_raw.strip().split('\n') if call]

# 获取配置信息
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

# 读取环境变量中的企业微信机器人的Webhook Key
WECHAT_ROBOT_KEY = os.getenv('WECHAT_ROBOT_KEY')
webhook_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={WECHAT_ROBOT_KEY}'

# 获取预警信息json地址
warning_info_url = os.getenv('WARNING_INFO_URL')

# 天气预警信息存储文件
# 获取当前脚本的目录  
script_dir = os.path.dirname(os.path.abspath(__file__))  
file_name = 'weather_warning_info.txt' 
# 构建完整的文件路径  
file_path = os.path.join(script_dir, file_name)  

# 获取预警信息
def get_weather_warning(warning_info_url):
    monitor_regions = ["渝中区", "江北区", "南岸区", "九龙坡区", "沙坪坝区", "大渡口区", "北碚区", "渝北区", "巴南区"] # 需要检查的地区列表
    warning_info = {
        "headline": "",     # 预警内容标题
        "description": "",      # 预警内容
        "sendTime": ""      # 预警发布时间
    }
    try:
        response = requests.get(warning_info_url, timeout=10)        # 使用GET请求，并设置超时时间
        response.encoding = 'utf-8'         # 改一下编码格式，不然返回就是空信息内容
        response.raise_for_status()     # 如果响应状态码不是200，将抛出异常
        json_data = response.json()     # 解析JSON数据

        for info in json_data.get('alertData', []):
            # if ('重庆市' in info.get('headline', '') or '重庆市' in info.get('description', '')) and '发布' in info.get('headline', ''):
            if any(region in info.get('headline', '') or region in info.get('description', '') for region in monitor_regions) and '发布' in info.get('headline', ''):
                warning_info['headline'] = info['headline']
                warning_info['description'] = info['description']
                warning_info['sendTime'] = info['sendTime']
                break
        if warning_info['headline'] == "":
            # print("提醒：现在一切正常，暂时没有预警信息。")
            return None  # 返回None表示没有预警信息
        
    except requests.exceptions.RequestException as e:
        print(f"出现错误: {e}")
    except json.JSONDecodeError:
        print("【警告】好像出问题了，因为无法解析JSON，请排查是不是网站凉了！")
    except KeyError as e:
        print(f"【警告】在JSON 数据中没有找到想要的键值：{e}")

    return warning_info

# 更新预警信息文件内容
def update_warning_info(warning_info, file_path):
    try:
        # 读取现有文件内容
        with open(file_path, 'r+', encoding='utf-8') as file:
            existing_description = file.read().strip()
        new_description = warning_info.get('description', '')
        # 如果文件中的内容与新的预警信息不一致
        if existing_description != new_description:
            # 写入新的预警信息
            with open(file_path, 'w', encoding='utf-8') as file:
                file.seek(0)  # 移动到文件开头
                file.truncate()  # 清空文件内容
                file.write(new_description)  # 写入新的描述和时间
                file.flush()  # 刷新文件缓冲确保内容被立即写入
            return True  # 返回True表示内容已更新，可以发送消息
        else:
            return False  # 返回False表示内容未更新，不需要发送消息
    except FileNotFoundError:
        # 如果文件不存在，创建文件并写入预警信息
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_description)
        return True

# 调用函数以获取预警信息
warning_info = get_weather_warning(warning_info_url)

# 企业微信通知（仅自己可见 - 为了获取通知运行情况）
def send_wechat_message(webhook_url, warning_info):
    weather_warning_message = f"-----🚨极端天气预警🚨------\n📢{warning_info['headline']}\n-------------------------------------\n📬️{warning_info['description']}\n-------------------------------------\n发布时间：{warning_info['sendTime']}"
    payload = {
        "msgtype": "text",
        "text": {
            "content": weather_warning_message
        }
    }
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)      # 发送POST请求到企业微信机器人
        if response.ok:
            print("【温馨提醒】极端天气预警消息发送成功！")
            # print(f"【预警通知】{warning_info['headline']}\n【预警信息】{warning_info['description']}\n【发布时间】{warning_info['sendTime']}")
        else:
            print(f"发送消息失败，错误码：{response.status_code}，错误信息：{response.text}")
    except requests.exceptions.RequestException as e:
        print(f"发送消息时出现错误: {e}")

# 初始化天气预报发送成功和失败的计数器
success_count = 0
failure_count = 0
# 初始化失败的ID列表
failed_bpjiid = []

# 检查预警信息是否已更新
warning_info_txt = False

# 发送天气预警信息，只有预警信息不为空才发送
if warning_info and isinstance(warning_info, dict) and 'description' in warning_info:
    print(f"【预警信息】{warning_info['description']}[{warning_info['sendTime']}]")
    warning_info_txt = update_warning_info(warning_info, file_path)
    if warning_info_txt:
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
                'msg': f"{warning_info['description']}[{STN}]"  # 获取预警信息的描述
            }

            # 将参数编码为URL查询字符串
            query_string = up.urlencode(params)

            # 完整的请求URL
            full_url = f"{url}?{query_string}"

            # 发送GET请求开始发天气预警
            response = requests.get(full_url)

            print(f"系统时间：{system_time}\n北京时间：{beijing_time}")
            if response.text == "0":
                success_count += 1  # 成功次数加1
                print(f"{call}：天气预警发送成功（{response.text}）！")
            else:
                failure_count += 1  # 失败次数加1
                failed_bpjiid.append(call)      # 将失败的ID添加到列表中
                print(f"{call}：天气预警发送失败：{response.text}！")
            print(f"提交信息：{full_url}")      # 主要为了查看终端是否发送成功

            # 等待一个延迟发送的随机时间（怕背不住）
            time.sleep(random.uniform(20, 30))        
        send_wechat_message(webhook_url, warning_info)
        print(f"发送成功：{success_count}个\n发送失败：{failure_count}个")
    else:
        print("【温馨提醒】预警信息无变化，暂不发送新通知。")        
else:
    print("【温馨提醒】现在一切正常，暂时没有预警信息。")

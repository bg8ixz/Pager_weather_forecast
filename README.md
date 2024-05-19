# 重庆46023传呼台 - 业余无线电台站
![Static Badge](https://img.shields.io/badge/MMDVM-46023-green)  |  ![Static Badge](https://img.shields.io/badge/%E9%87%8D%E5%BA%86%E6%97%A0%E7%BA%BF%E7%94%B5-%E4%BC%A0%E5%91%BC%E5%8F%B0-blue)  |  ![Static Badge](https://img.shields.io/badge/%E4%BC%A0%E5%91%BC%E5%8F%B0-%E5%A4%A9%E6%B0%94%E9%A2%84%E6%8A%A5-orange)  |  ![Static Badge](https://img.shields.io/badge/%E4%BC%A0%E5%91%BC%E5%8F%B0-%E5%A4%A9%E6%B0%94%E9%A2%84%E8%AD%A6-red)

## 文件说明
|  序号 |  文件名 |  用途 |
| :------------: | :------------: | :------------: |
|  1 |  BPJI_Auto_Weather.py |  自动发送既定区域每日天气预报到终端 |
|  2 |  BPJI_Weather_warning.py |  自动发送既定区域天气预警到终端 |
| 3  | weather_warning_info.txt  |  存储最新相关天气预警信息 |

## 使用注意
#### 需要参数
|  序号 |  名称 |  作用 |
| :------------: | :------------: | :------------: |
|  1 |  WECHAT_ROBOT_KEY |  企业微信机器人key |
| 2  |  CALL_NUMBER |  所需要发送的ID列表（每行一个） |
|  3 |  SEND_INFO |  发送信息JSON参数 |
|  4 |  WARNING_INFO_URL | 获取天气预警信息网址（返回结果为JSON格式）  |

#### 参数说明
　　在 GitHub 仓库中，进入右上角`Settings`，在侧边栏找到`Secrets and variables`，点击展开选择`Actions`，点击`New repository secret`，然后创建一个名为`SEND_INFO`的`Secret`，将 JSON 格式的信息字符串作为它的值，如下格式：  
```
[
  { "url": "http://xxxx.xxx/xxxx.do", "api_key": "5f3c2d89a470******98c34fa276b85c", "city_code": "101040100", "region": "重庆城区", "STN": "重庆46023传呼台"}
]
```
|序号|参数|说明|举例|
| :------------: | :------------: | :------------: | :------------: |
|1|url|发送服务Web端地址|请联系服务商|
|2|api_key|天气Web API KEY|a8765d2e3f9c410b86c57d14f3e02967|
|3|city_code|城市代码|[和风天气城市列表](https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv)|
|4|region|区域信息|重庆城区|
|5|STN|信息发送站点|重庆46023传呼台|

　　在 GitHub 仓库中，进入右上角`Settings`，在侧边栏找到`Secrets and variables`，点击展开选择`Actions`，点击`New repository secret`，然后创建一个名为`CALL_NUMBER`的`Secret`，将 ID 作为它的值（**每行一个**）。

## 致谢
|序号|呼号|备注|
| :------------: | :------------: | :------------: |
|1|BG8LAK|中继服务、天气预报服务|
|2|BD7EM|中继服务、天气预报服务|

###### 说明：本服务仅限重庆46023传呼台使用，其他平台尚未测试！

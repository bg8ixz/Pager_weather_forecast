# 重庆46023传呼台 - 自动天气预报
## 使用方法
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

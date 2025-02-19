import json
import requests
import time
from datetime import datetime
import schedule
url_qw = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6593ab79-7175-4e60-87fa-b3d9f06add78"
header = {"Content-Type": "application/json"}
#提醒人信息
mentioned_ids=["@all"]
#Tpad链接
new_weekly="https://www.tapd.cn/35572188/bugtrace/bugreports/stat_general/general/customreport-1135572188001001045"
close_weekly="https://www.tapd.cn/35572188/bugtrace/bugreports/stat_general/general/customreport-1135572188001001046"

# 发送文本
tempDataText = {
    "msgtype": "text",
    "text": {
        "content": "hello world",
        "mentioned_mobile_list": ["13501047401"],
        "mentioned_list":mentioned_ids
    },
}
# 发送图文
tempDataNews = {
    "msgtype": "news",
    "news": {
        "articles": [
            {
                "title": "图片1",
                "description": "描述",
                "url": "www.baidu.com",
                "picurl": "http://t15.baidu.com/it/u=2779524134,1407980405&fm=224&app=112&f=JPEG?w=500&h=500"
            }
        ],
        "mentioned_list": ["曾雪梅"],
        "mentioned_mobile_list": []
    }
}

# 编写markdown文本
tempDataMarkdown = {"msgtype": "markdown",
                    "markdown": {
                        "content": f"<font color=\"info\">本周新建缺陷数</font>[链接]({new_weekly})\n<font color=\"comment\">本周关闭缺陷数</font>[链接]({close_weekly})",
                        "mentioned_list": mentioned_ids,
						"mentioned_mobile_list": ["13501047401"]
                    }}

def post(url, data, headers):
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print("消息发送成功！")
    else:
        print(f"消息发送失败，错误信息：{response.json()}")
def send_message():
    # 检查是否为工作日（周一至周五）
    today = datetime.today().weekday()
    print(today)
    if today == 4:  # 0=周一, 4=周五
        print("发送消息...")
        post(url_qw, tempDataMarkdown, header)
    else:
        print("今天不是周五，跳过发送消息。")

# 定时任务：工作日周五下午2点触发
schedule.every().friday.at("14:00").do(send_message)
'''#打印当前时间用于调试
def print_time():
    print(f"当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")'''
# 主循环
if __name__ == "__main__":
    print("定时任务已启动，等待发送...")
#    schedule.every().seconds.do(print_time) # 调用任务当前执行的时间
    while True:
        schedule.run_pending()
        time.sleep(10)  # 每10秒检查一次

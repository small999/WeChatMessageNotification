import json
import requests
import time
from datetime import datetime
import schedule
import extractBugInfo
# 企业微信机器人 Webhook 地址
urlQW='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=bb710911-3502-4995-b483-91ce79d49a7a'
#urlQWTest= "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6593ab79-7175-4e60-87fa-b3d9f06add78"
# 请求头
header = {"Content-Type": "application/json"}
# 提醒人信息
mentioned_ids = ["@all"]
# 仪表盘的链接
chartURL = 'https://www.tapd.cn/my_dashboard/index?dashboard_id=1169493316001000999'
# tapd 的cookie值
cookie = 'tapdsession=17455468419ed66ee13197d060b41a9237584bfacc6f8d3dcb93bdff8892ab875490d93589; app_locale_name=zh_CN; __root_domain_v=.tapd.cn; _qddaz=QD.138245546846015; _qddab=3-9tkz21.m9w8f3mz; dsc-token=iabwhaOKP4SzWpaW; t_u=7a0be77ebd6c7a9ad203be368a956a3a27fc152589ab7252cd14ad1eedd130cb500c6048c4e20f506e2c47b6a4706fb03d126bb76bd8181f171c44351d8e7f9c80f5ab6f225bace0%7C1; t_cloud_login=13501047401; locale=zh_CN; _t_uid=1879302889; _t_crop=69493316; new_worktable=my_dashboard%7C%7C%7C; tapd_div=100_0; _wt=eyJ1aWQiOiIxODc5MzAyODg5IiwiY29tcGFueV9pZCI6IjY5NDkzMzE2IiwiZXhwIjoxNzQ1NTUzOTc1fQ%3D%3D.c71a18e9627387e48ea1751fcf08c82746b9a8bd83068f66a8cf5dc09e66b79f'
# tapd的新建和关闭的url地址
urlNew = 'https://www.tapd.cn/my_dashboard/ajax_get_card_detail/1169493316001004491?dashboard_id=1169493316001000999'
urlClose='https://www.tapd.cn/my_dashboard/ajax_get_card_detail/1169493316001004489?dashboard_id=1169493316001000999'
header = {
    "Content-Type": "text/html; charset=UTF-8",
    "cookie": cookie,
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
#初始周新建bug数
newData={'kailiang.qiu': 0, 'shuangwu.wang': 0, '曾雪梅': 0,'zhixin.wang':0}
#初始周关闭bug数
closeData={'kailiang.qiu': 0, 'shuangwu.wang': 0, '曾雪梅': 0,'zhixin.wang':0}
#调用周新建bug总数
newData1=extractBugInfo.getdata(urlNew,header,0)
#调用周关闭bug总数
closeData1=extractBugInfo.getdata(urlClose,header,1)

def dealDict(oldDict,newDict=None):
    '''
    #处理一下周新建和关闭bug数，以测试人员的维度
    :param oldDict:
    :param newDict:
    :return: 返回处理后最终数据
    '''
    for k,v in oldDict.items():
        if v>0:
            newDict[k]=v

dealDict(newData1,newData)
dealDict(closeData1,closeData)

'''
#以新建和关闭的维度，分别展示新建、关闭数
def convert(oldDict):
    new = {}
    for key in oldDict.keys():
        if key=="kailiang.qiu":
            new["邱开亮"]=oldDict[key]
        elif key=="shuangwu.wang":
            new["王双五"]=oldDict[key]
        elif key=="曾雪梅":
            new["曾雪梅"]=oldDict[key]
        elif key=="zhixin.wang":
            new["王志新"]=oldDict[key]
    return new

new=convert(newData)
close=convert(closeData)
print(f'本周关闭数是{close}，本周新建数量是{new}')
'''
# 发送 markdown 文本消息的数据
tempDataMarkdown = {
    "touser":"@all",
    "msgtype": "markdown",
    "markdown": {
        "content": f"**邱开亮**\n<font color=\"info\">新建:{newData['kailiang.qiu']}个，关闭：{closeData['kailiang.qiu']}个</font>\n**王双五**\n<font color=\"info\">新建:{newData['shuangwu.wang']}个，关闭：{closeData['shuangwu.wang']}个</font>\n**曾雪梅**\n<font color=\"info\">新建:{newData['曾雪梅']}个，关闭：{closeData['曾雪梅']}个</font>\n**王志新**\n<font color=\"info\">新建:{newData['zhixin.wang']}个，关闭：{closeData['zhixin.wang']}个</font>\n点击[链接]({chartURL})查看详细信息~",
    }
}
def send_message():
    """
    发送消息到企业微信
    """
    try:
        # 检查是否为工作日（周一至周五）
        today = datetime.today().weekday()
        print(f"当前星期: {today}")
        if today == 4:  # 0=周一, 4=周五
            print("发送消息...")
            response = requests.post(urlQW, data=json.dumps(tempDataMarkdown), headers=header)
            response.raise_for_status()
            print("消息发送成功！")
        else:
            print("今天不是周五，跳过发送消息。")
    except requests.RequestException as e:
        print(f"消息发送失败，错误信息：{e}")
    except Exception as e:
        print(f"发生未知错误：{e}")


# 定时任务：工作日周五下午 2 点触发
schedule.every().friday.at("16:00").do(send_message)

if __name__ == "__main__":
    print("定时任务已启动，等待发送...")
    while True:
        schedule.run_pending()
        time.sleep(10)  # 每 10 秒检查一次

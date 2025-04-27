import requests

#  cookie 值
cookie = 'tapdsession=17455468419ed66ee13197d060b41a9237584bfacc6f8d3dcb93bdff8892ab875490d93589; app_locale_name=zh_CN; __root_domain_v=.tapd.cn; _qddaz=QD.138245546846015; _qddab=3-9tkz21.m9w8f3mz; dsc-token=iabwhaOKP4SzWpaW; t_u=7a0be77ebd6c7a9ad203be368a956a3a27fc152589ab7252cd14ad1eedd130cb500c6048c4e20f506e2c47b6a4706fb03d126bb76bd8181f171c44351d8e7f9c80f5ab6f225bace0%7C1; t_cloud_login=13501047401; locale=zh_CN; _t_uid=1879302889; _t_crop=69493316; new_worktable=my_dashboard%7C%7C%7C; tapd_div=100_0; _wt=eyJ1aWQiOiIxODc5MzAyODg5IiwiY29tcGFueV9pZCI6IjY5NDkzMzE2IiwiZXhwIjoxNzQ1NTUzOTc1fQ%3D%3D.c71a18e9627387e48ea1751fcf08c82746b9a8bd83068f66a8cf5dc09e66b79f'
# tapd的url地址
url_close = 'https://www.tapd.cn/my_dashboard/ajax_get_card_detail/1169493316001004489?dashboard_id=1169493316001000999'
url_new= 'https://www.tapd.cn/my_dashboard/ajax_get_card_detail/1169493316001004491?dashboard_id=1169493316001000999'

header = {
    "Content-Type": "text/html; charset=UTF-8",
    "cookie": cookie,
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

def getdata(url,header,type):
    '''
    :param url: 分别对应新建和关闭链接
    :param header:
    :param type: 0表示获取新建数据，传0表示取关闭数据
    :return:
    '''
    try:
        with requests.Session() as session:
            response = session.post(url, headers=header)
            response.raise_for_status()  # 检查响应状态码，如果不是 200 会抛出异常
            data = response.json()
            try:
                if type==0:
                    series_data=data["data"]["chart"]["series"][0]["data"]
                elif type==1:
                    series_data=data["data"]["chart"]["series"][5]["data"]
                xAxis_categories= data["data"]["chart"]["xAxis"]["categories"]
                result=dict(zip(xAxis_categories,series_data))#把数据的名字和bug数据转化为字典样式
                return result
            except (KeyError, IndexError):
                print("响应数据结构不符合预期，无法提取所需数据。")
                return None
    except requests.RequestException as e:
        print(f"请求失败，错误信息: {e}")
        return None
    except ValueError:
        print("响应内容不是有效的 JSON 格式。")
        return None
getdata(url_new,header,0)

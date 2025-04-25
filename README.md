需要安装以下包
pip install schedule1.2.2
pip install requests2.32.3

Tapd Bug 数据获取工具
一、项目概述
本项目是一个用于从 Tapd 平台特定接口提取新建和关闭 Bug 统计数据的 Python 脚本。它能够将获取的数据整理成字典形式，以日期为键，对应日期的 Bug 数量为值，方便后续的数据分析和项目监控。
二、功能特性
从 Tapd 接口获取新建和关闭 Bug 的统计数据。
对获取的数据进行解析和整理，生成日期与 Bug 数量对应的字典。
三、使用方法
1. 环境准备
确保你已经安装了 Python 环境（建议 Python 3.6 及以上版本），并安装了 requests 库。可以使用以下命令进行安装：
bash
pip install requests
2. 配置信息
打开代码文件，找到以下配置信息并进行相应修改：
python
#  cookie 值
cookie = 'your_tapd_cookie'
# tapd的url地址
url_close = 'https://www.tapd.cn/my_dashboard/ajax_get_card_detail/1169493316001004489?dashboard_id=1169493316001000999'
url_new= 'https://www.tapd.cn/my_dashboard/ajax_get_card_detail/1169493316001004491?dashboard_id=1169493316001000999'

header = {
    "Content-Type": "text/html; charset=UTF-8",
    "cookie": cookie,
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
cookie：替换为你自己登录 Tapd 后的有效 cookie 值。
url_close 和 url_new：如果 Tapd 接口地址有变化，需要更新为正确的地址。
3. 运行脚本
在终端中进入项目所在目录，运行以下命令：
bash
python your_script_name.py

将 your_script_name.py 替换为实际的脚本文件名。
四、注意事项
Cookie 有效期：代码中使用的 Cookie 有一定的有效期，过期后需要重新获取。
接口变更：如果 Tapd 的接口地址或响应数据结构发生变化，代码需要相应地进行调整。

import requests
import chardet
import os
import json

# 从青龙面板的环境变量中读取 cookie
rili_cookie = os.environ.get("rili_cookie")

if not rili_cookie:
    print("❌ 环境变量 rili_cookie 未设置")
    exit(1)

# 配置参数
url = "http://event.inh5.cn/rili_hidesign/Hand/vipcenter/signinday.html"

# 微信客户端 User-Agent（需定期更新）
wechat_ua = (
    "Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 "
    "XWEB/4313 MMWEBSDK/20241202 Mobile Safari/537.36 "
    "MMWEBID/9433 MicroMessenger/8.0.27.2220(0x28001B53) "
    "WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
)

headers = {
    "Host": "event.inh5.cn",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "User-Agent": wechat_ua,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "http://event.inh5.cn",
    "Referer": "http://event.inh5.cn/rili_hidesign/Hand/vipcenter?t=1738586883498",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": rili_cookie
}

def sign_in():
    try:
        # 发送 POST 请求
        response = requests.post(
            url,
            headers=headers,
            data=None,
            timeout=10
        )

        # 检查响应状态码
        if response.status_code == 200:
            # 自动检测编码并解码
            encoding = chardet.detect(response.content)['encoding'] or 'utf-8'
            decoded_data = response.content.decode(encoding)

            # 尝试解析 JSON 数据
            try:
                json_data = json.loads(decoded_data)
                if "msg" in json_data:
                    # 打印 msg 内容
                    print("签到结果:", json_data["msg"])
                else:
                    print("未找到 msg 字段")
            except json.JSONDecodeError:
                print("响应内容不是有效的 JSON 格式:", decoded_data[:100])  # 打印前100字符

        else:
            print(f"服务器返回状态码: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("请求异常:", str(e))

if __name__ == "__main__":
    sign_in()

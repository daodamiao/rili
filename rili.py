import requests
import os
import json
import chardet

# 从青龙面板的环境变量中读取 cookie
rili_cookie = os.environ.get("rili_cookie")

if not rili_cookie:
    print("❌ 环境变量 rili_cookie 未设置")
    exit(1)

# 配置参数
url = "http://event.inh5.cn/rili_hidesign/Hand/vipcenter/signinday.html"

# 微信客户端 User-Agent（需定期更新）
headers = {
    "Host": "event.inh5.cn",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Content-Length": "0",
    "User-Agent": "Mozilla/5.0 (Linux; Android 15; 23113RKC6C Build/AQ3A.240912.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.103 Mobile Safari/537.36 XWEB/1300333 MMWEBSDK/20241202 MMWEBID/4269 MicroMessenger/8.0.56.2800(0x28003855) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": rili_cookie
}

def sign_in():
    x_requested_with_values = ["XMLHttpRequest", "com.tencent.mm"]  # 可用的 X-Requested-With 值
    current_index = 0  # 当前使用的索引

    while current_index < len(x_requested_with_values):
        headers["X-Requested-With"] = x_requested_with_values[current_index]
        try:
            # 发送 GET 请求
            response = requests.get(
                url,
                headers=headers,
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

                    if json_data.get("result") == "ok":
                        # 签到成功
                        msg = json_data.get("msg", {}).get("msg", "未知消息")
                        points = json_data.get("msg", {}).get("points", "无积分信息")
                        print(f" 👌 签到成功: {msg}")
                        print(f"🎁 获得签到积分: {points}")
                        return  # 成功后退出函数
                    elif json_data.get("result") == "err":
                        # 已经签到过
                        msg = json_data.get("msg", "未知错误")
                        print(f"❗❗❗ : {msg}")
                        return  # 已签到后退出函数
                    else:
                        print("未知的响应结果:", decoded_data)

                except json.JSONDecodeError:
                    print("响应内容不是有效的 JSON 格式:", decoded_data[:100])  # 打印前100字符

            else:
                print(f"❌❌❌服务器返回状态码: {response.status_code}")
                print("响应内容:", response.text[:100])  # 打印前100字符

                if response.status_code == 404:
                    # 如果状态码为 404，切换 X-Requested-With 的值
                    if current_index < len(x_requested_with_values) - 1:
                        current_index += 1
                        print(f"切换 X-Requested-With 为: {x_requested_with_values[current_index]}")
                        continue  # 重新尝试请求
                    else:
                        print("所有 X-Requested-With 值已尝试，无法继续切换")
                        break  # 退出循环

            break  # 正常退出循环

        except requests.exceptions.RequestException as e:
            print("请求异常:", str(e))
            break  # 异常情况下退出循环

if __name__ == "__main__":
    sign_in()

import requests
import time

# 获取当前时间戳
current_timestamp = int(time.time())

# 将时间戳作为变量传入URL
url = f"https://portal.gcable.cn:8084/PortalServer-App/new/ptl_ipvp_live_live005?categoryID=0&channelName=&countyName=&end=1000&locationName=&pappName=GoodTV&pkv=1&plocation=1601&programName=&pserialNumber=c4e9ad95722e8fc64271c36c8e0ea687&pserverAddress=portal.gcable.cn&ptoken=dzsUJ2K3evgfZHJ6Ub6W2w%253D%253D&ptype=3&puser=18925918576&pversion=030107&sortType=2&sscert=true&start=0&timestamp={current_timestamp}&version=v3.5.0%283431%29"

# 发送GET请求并获取响应
response = requests.get(url)

# 检查响应是否成功
if response.status_code == 200:
    data = response.json()
    
    # 检查是否存在channelInfos键
    if "channelInfos" in data["data"]:
        channel_infos = data["data"]["channelInfos"]
        
        # 创建或打开文件 gudou_channel_id_1601.txt 以便写入数据
        with open("gudou_channel_id_1601.txt", "w", encoding="utf-8") as file:
            channel_count = 0  # 初始化带播放链接的频道计数
            
            # 遍历所有频道信息
            for channel_info in channel_infos:
                channel_name = channel_info.get("channelName", "N/A")
                channel_id = channel_info.get("channelID", "N/A")
                
                # 获取频道URL（选择第一个URL）
                channel_urls = channel_info.get("channelUrl", [])
                if channel_urls:
                    channel_url = channel_urls[0]
                    channel_count += 1  # 如果有播放链接，增加计数
                else:
                    channel_url = "N/A"
                
                # 将频道信息写入文件
                file.write(f"频道名称: {channel_name}\n")
                file.write(f"频道ID: {channel_id}\n")
                file.write(f"播放链接: {channel_url}\n\n")
            
            # 输出带播放链接的频道数量
            print(f"总共有 {channel_count} 个带播放链接的频道。")
    else:
        print("找不到频道信息。")
else:
    print(f"请求失败，状态码: {response.status_code}")

print("结果已保存到 gudou_channel_id_1601.txt 文件.")

# 读取TXT文件内容
with open("gudou_channel_id_1601.txt", "r", encoding="utf-8") as txt_file:
    lines = txt_file.readlines()

# 创建M3U文件并写入内容
with open("gudou_channels_1601.m3u.txt", "w", encoding="utf-8") as m3u_file:
    channel_info = {}  # 初始化频道信息字典

    for line in lines:
        line = line.strip()
        if line.startswith("频道名称: "):
            channel_info["name"] = line.replace("频道名称: ", "")
        elif line.startswith("播放链接: "):
            url_line = line.replace("播放链接: ", "")
            if url_line != "N/A":
                try:
                    channel_url_dict = eval(url_line)
                    # 检查字典中是否有键 "3"，然后访问对应的播放链接
                    if "3" in channel_url_dict:
                        channel_info["url"] = channel_url_dict["3"]
                        # 替换播放链接部分
                        channel_info["url"] = channel_info["url"].replace("http://gslb.gcable.cn:8070/live/", "http://192.168.6.3/tv/php/gudou.php?id=")
                        m3u_file.write(f"#EXTINF:-1,{channel_info['name']}\n")
                        m3u_file.write(f"{channel_info['url']}\n")
                except Exception as e:
                    pass

print("M3U文件 gudou_channels_1601.m3u.txt 已生成并替换播放链接。")
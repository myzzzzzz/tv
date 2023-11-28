import requests
import time

# 获取当前时间戳
current_timestamp = int(time.time())

# 遍历两个地理位置
plocations = ["001", "1601"]

# 用于存储所有频道信息的列表
all_channels = []

# 遍历不同地理位置
for plocation in plocations:
    # 构建URL
    url = f"https://portal.gcable.cn:8084/PortalServer-App/new/ptl_ipvp_live_live005?categoryID=0&channelName=&countyName=&end=1000&locationName=&pappName=GoodTV&pkv=1&plocation={plocation}&programName=&pserialNumber=c4e9ad95722e8fc64271c36c8e0ea687&pserverAddress=portal.gcable.cn&ptoken=dzsUJ2K3evgfZHJ6Ub6W2w%253D%253D&ptype=3&puser=18925918576&pversion=030107&sortType=2&sscert=true&start=0&timestamp={current_timestamp}&version=v3.5.0%283431%29"
    
    # 发送GET请求并获取响应
    response = requests.get(url)
    
    # 检查响应是否成功
    if response.status_code == 200:
        data = response.json()
        
        # 检查是否存在channelInfos键
        if "channelInfos" in data["data"]:
            channel_infos = data["data"]["channelInfos"]
            
            # 遍历所有频道信息
            for channel_info in channel_infos:
                channel_id = channel_info.get("channelID", "N/A")
                
                # 检查频道是否已经存在，如果不存在则添加到列表中
                if channel_id not in all_channels:
                    all_channels.append(channel_id)
                    
                    # 这里可以继续处理频道信息，例如写入文件或其他操作
        else:
            print(f"找不到频道信息。 (plocation={plocation})")
    else:
        print(f"请求失败，状态码: {response.status_code} (plocation={plocation})")

# 将所有频道信息写入TXT文件
with open("gudou_all_channels.txt", "w", encoding="utf-8") as txt_file:
    with open("gudou_all_channels.m3u", "w", encoding="utf-8") as m3u_file:
        channel_count = 0  # 初始化带播放链接的频道计数
        
        # 遍历所有频道信息
        for channel_id in all_channels:
            # 获取频道信息
            url = f"https://portal.gcable.cn:8084/PortalServer-App/new/ptl_ipvp_live_live005?categoryID=0&channelID={channel_id}&end=1000&locationName=&pappName=GoodTV&pkv=1&plocation=001&programName=&pserialNumber=c4e9ad95722e8fc64271c36c8e0ea687&pserverAddress=portal.gcable.cn&ptoken=dzsUJ2K3evgfZHJ6Ub6W2w%253D%253D&ptype=3&puser=18925918576&pversion=030107&sortType=2&sscert=true&start=0&timestamp={current_timestamp}&version=v3.5.0%283431%29"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                channel_info = data["data"]["channelInfos"][0]
                channel_name = channel_info.get("channelName", "N/A")
                channel_url = channel_info.get("channelUrl", ["N/A"])[0]
                
                # 将频道信息写入TXT文件
                txt_file.write(f"频道名称: {channel_name}\n")
                txt_file.write(f"频道ID: {channel_id}\n")
                txt_file.write(f"播放链接: {channel_url}\n\n")
                
                # 将频道信息写入M3U文件
                m3u_file.write(f"#EXTINF:-1,频道名称: {channel_name}\n")
                m3u_file.write(f"#EXTINF:-1,频道ID: {channel_id}\n")
                m3u_file.write(f"#EXTINF:-1,播放链接: {channel_url}\n")
                m3u_file.write(f"http://192.168.6.3/tv/php/gudou.php?id={channel_id}\n")
                
                channel_count += 1
            
        # 输出带播放链接的频道数量
        print(f"总共有 {channel_count} 个带播放链接的频道。")

# 输出总共的频道数量
print(f"总共有 {len(all_channels)} 个频道。")

import requests
import xml.etree.ElementTree as ET
import datetime
import os
from bs4 import BeautifulSoup as bs

# 定义一个整数变量channel_id，赋值为2
channel_id = 2

# 使用变量channel_id来拼接URL
url = f"https://apip01.rthk.hk/assets/schedule/rthk_radio{channel_id}_schedule.xml"

# 定义一个函数get_epgs_radiorthk，用于获取指定日期和频道的EPG信息
def get_epgs_radiorthk(channel, channel_id, dt, func_arg):
    epgs = []
    msg = ''
    success = 1
    need_date = dt.strftime('%Y%m%d')
    try:
        res = requests.get(url, timeout=5)
        res.encoding = 'utf-8'
        root = ET.fromstring(res.text)
        prog_lists = root.findall("program")
        for prog_list in prog_lists:
            title = prog_list.find("title").text
            description = prog_list.find("description").text
            presenter = prog_list.find("presenter").text
            showtime = prog_list.find("showtime").text

            # Split the showtime into start_time and end_time
            start_time, end_time = showtime.split("-")

            # Add seconds part ":00"
            start_time += ":00"
            end_time += ":00"

            # Modify time format to "yyyyMMddHHmmss"
            start_datetime = datetime.datetime.strptime(need_date + start_time, '%Y%m%d%H:%M:%S')
            end_datetime = datetime.datetime.strptime(need_date + end_time, '%Y%m%d%H:%M:%S')

            epg = {
                'channel_id': channel_id,
                'starttime': start_datetime,
                'endtime': end_datetime,
                'title': title,
                'desc': description,
                'presenter': presenter,
                'program_date': dt,
            }
            epgs.append(epg)
        epglen = len(epgs)
    except Exception as e:
        success = 0
        spidername = os.path.basename(__file__).split('.')[0]
        msg = f'spider-{spidername} - {e}'
    ret = {
        'success': success,
        'epgs': epgs,
        'msg': msg,
        'last_program_date': dt,
        'ban': 0,
    }
    return ret

# 其余部分不需要修改，保持不变

# 定义一个函数get_channels_radiorthk，用于获取所有可用频道的信息
def get_channels_radiorthk():
    channels = []
    host = "https://www.rthk.hk"
    url = f"{host}/radio/radio{channel_id}/programme"
    res = requests.get(url, timeout=5)
    res.encoding = 'utf-8'
    soup = bs(res.text, 'html.parser')
    divs = soup.select('div.programmeList > div')
    for div in divs:
        name = div.select('h3 > a')[0].text.strip()
        id = div.select('h3 > a')[0].attrs['href'].split('/')[-1]
        logo = host + div.select('img')[0].attrs['src']
        desc = div.select('p')[0].text.strip()
        channel = {
            'name': name,
            'id': [id],
            'url': f"{host}/radio/radio{channel_id}/programme/{id}",
            'source': 'rthk',
            'logo': logo,
            'desc': desc,
            'sort': '香港',
        }
        channels.append(channel)
    return channels
# -*- coding:utf-8 -*-
import requests
import re
import datetime
import json
import os
from utils.general import headers
from bs4 import BeautifulSoup as bs

def get_epgs_rthkradio(channel, channel_id, dt, func_arg):
    epgs = []
    msg = ''
    success = 1
    need_date = dt.strftime('%Y%m%d')
    url = f'https://apip01.rthk.hk/assets/schedule/rthk_radio{channel_id}_schedule.xml'
    
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res.encoding = 'utf-8'
        xml_content = res.text

        # 使用 BeautifulSoup 解析XML数据
        soup = bs(xml_content, 'xml')
        programs = soup.find_all('program')

        for program in programs:
            title = program.title.text
            presenter = program.presenter.text
            showtime = program.showtime.text

            # 解析showtime以分离开始和结束时间
            start_time, end_time = showtime.split('-')

            starttime = datetime.datetime.strptime(start_time, '%H:%M')
            endtime = datetime.datetime.strptime(end_time, '%H:%M')

            epg = {
                'channel_id': channel.id,
                'starttime': starttime,
                'endtime': endtime,
                'title': title,
                'desc': '',
                'program_date': dt,
            }
            epgs.append(epg)

    except Exception as e:
        success = 0
        spidername = os.path.basename(__file__).split('.')[0]
        msg = f'spider-{spidername}- {e}'

    ret = {
        'success': success,
        'epgs': epgs,
        'msg': msg,
        'last_program_date': dt,
        'ban': 0,
    }
    return ret

def get_channels_rthkradio():
    channels = []

    # 在这里编写代码来获取RTHK Radio的频道信息
    # 请根据实际情况构建URL和解析相应的数据
    # 将获取的频道信息添加到channels列表中
    # 注意：你需要提供实际的频道信息

    # 示例：
    channel_id = 1  # 假设频道ID为1
    channel_url = f'https://apip01.rthk.hk/assets/schedule/rthk_radio{channel_id}_schedule.xml'

    # 获取频道信息
    channel_response = requests.get(channel_url, headers=headers, timeout=5)
    channel_response.encoding = 'utf-8'
    channel_data = bs(channel_response.text, 'xml')

    # 从channel_data中提取频道信息
    channel_name = channel_data.channel.name.text
    channel_id = channel_data.channel.id.text
    channel_url = channel_data.channel.link.text
    channel_logo = channel_data.channel.logo.text

    channel = {
        'name': channel_name,
        'id': channel_id,
        'url': channel_url,
        'source': 'rthk',
        'logo': channel_logo,
        'desc': '',
        'sort': 'RTHK Radio 1',  # 根据频道实际情况
    }
    channels.append(channel)

    return channels
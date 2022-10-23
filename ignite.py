import textwrap
import time

import requests
import json
import datetime
import streamlit as st
from st_on_hover_tabs import on_hover_tabs
import pyshorteners as ps

# 获取Authorization

headers2 = {
    'Accept': '*/*',
    'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
    'Accept-Language': 'zh-Hans-JP;q=1.0, ja-JP;q=0.9, en-JP;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'api.n46.glastonr.net',
    'User-Agent': 'Hot/1.4.00 (jp.co.sonymusic.communication.nogizaka; build:136; iOS 15.5.0) Alamofire/5.6.2',
    'X-Talk-App-ID': 'jp.co.sonymusic.communication.nogizaka 2.2',
}

r_token = {
    "refresh_token": "4dfeaece-a031-4409-ae68-ae532fd1406e"
}

url1 = 'https://api.n46.glastonr.net/v2/update_token'

respones1 = json.loads(requests.post(url1, headers=headers2, json=r_token).text)

access_token = respones1['access_token']

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
    'Accept-Language': 'zh-Hans-JP;q=1.0, ja-JP;q=0.9, en-JP;q=0.8',
    'Authorization': f'Bearer {access_token}',
    'Connection': 'keep-alive',
    'Host': 'api.n46.glastonr.net',
    'User-Agent': 'Hot/1.4.00 (jp.co.sonymusic.communication.nogizaka; build:136; iOS 15.5.0) Alamofire/5.6.2',
    'X-Talk-App-ID': 'jp.co.sonymusic.communication.nogizaka 2.2',
}

# MSG部分
st.set_page_config(
    page_title="Ignite订阅的MSG",
)
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

tabname = ['山下美月', '久保史緒里', '松尾美佑']
iconname = ['grain', 'grain', 'grain', 'grain', 'grain', 'grain', 'grain', 'grain', 'grain']
styles = {'tabStyle' : {'list-style-type': 'none','margin-bottom': '10px','padding-left': '20px'}}

with st.sidebar:
    tabs = on_hover_tabs(tabName=tabname,iconName=iconname, default_choice=0,styles = styles,key =1 )


# 缩短网址
def short(video_url):
    u = ps.Shortener().dagd.short(video_url)
    return u

def msg():
    st.subheader(tabs)

    url = f'https://api.n46.glastonr.net/v2/groups/{member_id}/timeline?count=200&order=desc'

    r = requests.get(url, headers=headers).text

    r = json.loads(r)

    r = r["messages"]

    i = 0
    for msg in r:

        # 时间
        date = r[i]["updated_at"]
        t = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        tt = datetime.timedelta(hours=9)
        ttt = (t + tt)
        tttt = datetime.datetime.strftime(ttt, "%Y年%m月%d日 %H:%M:%S")

        # 类型
        r_type = r[i]['type']
        if r[i]["state"] == "canceled":
            break
        # 语音
        if r_type == 'voice':
            st.caption(f'{tttt}')
            r_audio = r[i]['file']
            st.audio(r_audio, format='audio/m4a')
            st.caption(f'下载音频:{short(r_audio)}')
            st.text('\n\n')
        # 视频
        if r_type == 'video':
            r_video = r[i]['file']
            st.caption(f'{tttt}')
            st.video(r_video, format='video/mp4')
            st.caption(f'下载视频:{short(r_video)}')
            st.text('\n\n')
        # 图片
        if r_type == 'picture':
            if 'text' in r[i]:
                text = r[i]["text"]
                r_pic = r[i]['file']
                st.caption(f'{tttt}')
                st.text(text)
                st.image(r_pic, width=300)
                st.text('\n\n')
            else:
                r_pic = r[i]['file']
                st.caption(f'{tttt}')
                st.image(r_pic, width=300)
                st.text('\n\n')

        # 文本
        if r_type == 'text':
            text = r[i]["text"]
            st.caption(f'{tttt}')
            st.text(text)
            st.text('\n\n')
        i += 1
        continue


if tabs == '松尾美佑':
    member_id = 42
    msg()
if tabs == '久保史緒里':
    member_id = 21
    msg()
if tabs == '山下美月':
    member_id = 26
    msg()


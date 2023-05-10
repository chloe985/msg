import textwrap
import time

import requests
import json
import datetime
import streamlit as st
import pyshorteners as ps
import streamlit.components.v1 as components


#获取Authorization
headers2={
    'Accept': '*/*',
    'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
    'Accept-Language': 'zh-Hans-JP;q=1.0, ja-JP;q=0.9, en-JP;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'api.n46.glastonr.net',
    'User-Agent': 'Hot/1.4.00 (jp.co.sonymusic.communication.nogizaka; build:136; iOS 15.5.0) Alamofire/5.6.2',
    'X-Talk-App-ID': 'jp.co.sonymusic.communication.nogizaka 2.2',
}

r_token={
  "refresh_token": "3789acbf-32b8-4b59-b5d3-7ba416bdeb89"
}

url2 = f'https://api.n46.glastonr.net/v2/update_token'

respones = json.loads(requests.post(url2, headers=headers2,json=r_token).text)

access_token = respones['access_token']

#MSG部分

headers={
    'Accept': '*/*',
    'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
    'Accept-Language': 'zh-Hans-JP;q=1.0, ja-JP;q=0.9, en-JP;q=0.8',
    'Authorization': f'Bearer {access_token}',
    'Connection': 'keep-alive',
    'Host': 'api.n46.glastonr.net',
    'User-Agent': 'Hot/1.4.00 (jp.co.sonymusic.communication.nogizaka; build:136; iOS 15.5.0) Alamofire/5.6.2',
    'X-Talk-App-ID': 'jp.co.sonymusic.communication.nogizaka 2.2',
}

st.set_page_config(page_title="Ignite")

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

col1, col2= st.columns(2,gap="medium")



with col1:
    option = st.sidebar.selectbox('选择成员',
                                  ('山下美月', '久保史绪里', '松尾美佑', '乃木坂46'))
    yesterday_ = datetime.datetime.now() + datetime.timedelta(days = -7)
    datebox = st.sidebar.date_input('选择MSG查询日期(手机端推荐手动输入)',yesterday_)
    checkbox = st.sidebar.checkbox('正序',value=False)
    st.sidebar.caption('★若要按照日期查询,务必先勾选 **[正序]**')
    st.sidebar.caption('★取消勾选 **[正序]** 后回到默认显示状态')
    count_ = st.sidebar.text_input('输入MSG显示数量(1~200)',value="20")
    st.sidebar.caption('★默认显示最新的**20条**')

url_group = 'https://api.n46.glastonr.net/v2/groups'

response = requests.get(url_group, headers=headers)

group_r = json.loads(response.text)

group_n = {}

def group(idid):

    global group_n

    i = 0

    for num in group_r:

        id = group_r[i]['id']

        name = group_r[i]['name']

        group_n=({id:name})

        i+=1

        if idid == id:
            id_name =group_n[idid]
            return id_name

# 缩短网址
def short(video_url):
    u = ps.Shortener().dagd.short(video_url)
    return u

with col2:

    def msg():
        st.subheader(option)

        url_more = []

        if checkbox == False:
            url_more = f'order=desc'
        if checkbox == True:
            url_more = f'created_from={datebox}T09:00:00Z'

        url = f'https://api.n46.glastonr.net/v2/groups/{member_id}/timeline?&count={count_}&{url_more}'

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
            tttt = datetime.datetime.strftime(ttt, "%Y年%m月%d日 %H:%M")

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

    # 乃木坂46公屏
    def ngzk46():
        st.subheader(option)

        url_more = []

        if checkbox == False:
            url_more = f'order=desc'
        if checkbox == True:
            url_more = f'created_from={datebox}T09:00:00Z'

        url = f'https://api.n46.glastonr.net/v2/groups/{member_id}/timeline?&count={count_}&{url_more}'

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
            tttt = datetime.datetime.strftime(ttt, "%Y年%m月%d日 %H:%M")

            group_id = r[i]["group_id"]
            member_ids = r[i]["member_id"]

            # 类型
            r_type = r[i]['type']
            if r[i]["state"] == "canceled":
                break
            # 语音
            if r_type == 'voice':
                st.caption(f'{group(member_ids)} {tttt}')
                r_audio = r[i]['file']
                st.audio(r_audio, format='audio/m4a')
                st.caption(f'下载音频:{short(r_audio)}')
                st.text('\n')
            # 视频
            if r_type == 'video':
                r_video = r[i]['file']
                st.caption(f'{group(member_ids)} {tttt}')
                st.video(r_video, format='video/mp4')
                st.caption(f'下载视频:{short(r_video)}')
                st.text('\n')
            # 图片
            if r_type == 'picture':
                if 'member_id' in r[i] and 'group_id' in r[i]:
                    if 'text' in r[i]:
                        text = r[i]["text"]
                        r_pic = r[i]['file']
                        st.caption(f'{group(member_ids)} {tttt}')
                        st.text(text)
                        st.image(r_pic, width=300)
                        st.text('\n')
                    else:
                        r_pic = r[i]['file']
                        st.caption(f'{group(member_ids)} {tttt}')
                        st.image(r_pic, width=300)
                        st.text('\n')
                if 'member_id' not in r[i] and 'group_id' in r[i]:
                    if 'text' in r[i]:
                        text = r[i]["text"]
                        r_pic = r[i]['file']
                        st.caption(f'{group(group_id)} {tttt}')
                        st.text(text)
                        st.image(r_pic, width=300)
                        st.text('\n')
                    else:
                        r_pic = r[i]['file']
                        st.caption(f'{group(group_id)} {tttt}')
                        st.image(r_pic, width=300)
                        st.text('\n')

            # 文本
            if r_type == 'text':
                if 'member_id' in r[i] and 'group_id' in r[i]:
                    text = r[i]["text"]
                    st.caption(f'{group(member_ids)} {tttt}')
                    st.text(text)
                    st.text('\n')
                if 'member_id' not in r[i] and 'group_id' in r[i]:
                    text = r[i]["text"]
                    st.caption(f'{group(group_id)} {tttt}')
                    st.text(text)
                    st.text('\n')
            i += 1
            continue


if option == '久保史绪里':
    member_id = 21
    msg()
if option == '山下美月':
    member_id = 26
    msg()
if option == '松尾美佑':
    member_id = 42
    msg()

if option == '乃木坂46':
    member_id = 45
    ngzk46()

import requests

cookies = {
    'buvid3': 'D3E099FF-A23F-CEB3-7A1A-874159BD69BD12937infoc',
    'rpdid': '|(kmJY|kYk|~0J\'uYk~lRmuul',
    'video_page_version': 'v_old_home',
    'LIVE_BUVID': 'AUTO3916383602607414',
    'fingerprint': '3956dc0c9167d24fe6fca360d44a1545',
    'fingerprint_s': '3b87c45c5eafb420dc308298057fa1e5',
    'buvid4': '50A7DFC0-AC53-FD96-A661-5D9B7FAF2D5569566-022012119-AiqhsCVq4sg4t9myV8sjiA%3D%3D',
    'i-wanna-go-back': '-1',
    'buvid_fp_plain': 'undefined',
    'DedeUserID': '500022342',
    'DedeUserID__ckMd5': 'ae92aad31ed32a04',
    'b_ut': '5',
    'buvid_fp': '3956dc0c9167d24fe6fca360d44a1545',
    'CURRENT_BLACKGAP': '0',
    'nostalgia_conf': '-1',
    'hit-dyn-v2': '1',
    'fingerprint3': '55e1884cd21ae77683b4f634379f057c',
    'blackside_state': '0',
    '_uuid': 'B41DC577-138A-3FC3-35BB-9AB105C13131E73696infoc',
    'CURRENT_QUALITY': '0',
    'SESSDATA': 'df9fe279%2C1675404939%2C79c2f%2A81',
    'bili_jct': 'be624c0e72ed1c312cd0fc4504f968ee',
    'PVID': '1',
    'bp_video_offset_500022342': '692250644207108100',
    'innersign': '0',
    'b_lsid': '4910B2684_18297157116',
    'bsource': 'search_baidu',
    'b_timer': '%7B%22ffp%22%3A%7B%22333.1007.fp.risk_D3E099FF%22%3A%2218297157319%22%2C%22333.1193.fp.risk_D3E099FF'
               '%22%3A%221829715772E%22%2C%22333.934.fp.risk_D3E099FF%22%3A%22182971598A3%22%7D%7D',
}

headers = {
    'authority': 'api.bilibili.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # Requests sorts cookies= alphabetically 'cookie': 'buvid3=D3E099FF-A23F-CEB3-7A1A-874159BD69BD12937infoc;
    # rpdid=|(kmJY|kYk|~0J\'uYk~lRmuul; video_page_version=v_old_home; LIVE_BUVID=AUTO3916383602607414;
    # fingerprint=3956dc0c9167d24fe6fca360d44a1545; fingerprint_s=3b87c45c5eafb420dc308298057fa1e5;
    # buvid4=50A7DFC0-AC53-FD96-A661-5D9B7FAF2D5569566-022012119-AiqhsCVq4sg4t9myV8sjiA%3D%3D; i-wanna-go-back=-1;
    # buvid_fp_plain=undefined; DedeUserID=500022342; DedeUserID__ckMd5=ae92aad31ed32a04; b_ut=5;
    # buvid_fp=3956dc0c9167d24fe6fca360d44a1545; CURRENT_BLACKGAP=0; nostalgia_conf=-1; hit-dyn-v2=1;
    # fingerprint3=55e1884cd21ae77683b4f634379f057c; blackside_state=0;
    # _uuid=B41DC577-138A-3FC3-35BB-9AB105C13131E73696infoc; CURRENT_QUALITY=0;
    # SESSDATA=df9fe279%2C1675404939%2C79c2f%2A81; bili_jct=be624c0e72ed1c312cd0fc4504f968ee; PVID=1;
    # bp_video_offset_500022342=692250644207108100; innersign=0; b_lsid=4910B2684_18297157116; bsource=search_baidu;
    # b_timer=%7B%22ffp%22%3A%7B%22333.1007.fp.risk_D3E099FF%22%3A%2218297157319%22%2C%22333.1193.fp.risk_D3E099FF%22
    # %3A%221829715772E%22%2C%22333.934.fp.risk_D3E099FF%22%3A%22182971598A3%22%7D%7D',
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 '
                  'Safari/537.36',
}

params = {
    'ps': '20',
    'pn': '1',
}

response = requests.get('https://api.bilibili.com/x/web-interface/popular', params=params, cookies=cookies, headers=headers)
datas=response.json()['data']['list']
print(len(datas))
results = []
for data in datas:
    if 'short_link' in data:
        short_link = data['short_link']
    else:
        short_link = ''
    result = {
        '标题': data['title'],
        '视频分类':data['tname'],
        'aid': data['aid'],
        'bvid': data['bvid'],
        '视频描述': data['desc'],
        '视频封面': data['pic'],
        'up主': data['owner']['name'],
        '视频链接': data.get('short_link'),
        '投币数': data['stat']['coin'],
        '收藏数': data['stat']['favorite'],
        '弹幕数': data['stat']['danmaku'],
        '喜欢数': data['stat']['like'],
        '观看数': data['stat']['view'],
        '分享数': data['stat']['share'],
    }
    results.append(result)
    print(result)
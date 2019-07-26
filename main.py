# Author : ZhangTong

import requests
import json
import re
import os

def download(url, retries=3):
    '''
    下载
    :param url:
    :param retries:重试次数
    :return: 下载内容
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    try:
        r = requests.get(url,headers=headers)
        if r.status_code == 200:
            return r.text
    except:
        return download(url, retries-1)

def download_img(url):
    '''
    下载图片
    :param url: 图片地址
    :return: 二进制数据
    '''
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
    except:
        print('下载图片失败TNT')

def parse_1(html):
    '''
    解析初始页面
    :param html: 初始页面的响应内容
    :return: 每个英雄的英文名(构造下一级网页)和对应中文名
    '''
    id1 = []
    name1 = []
    dct = re.search('{\n\t"data".*}', html, re.S).group()
    dct = json.loads(dct)
    data = dct['data']
    for k in data:
        id1.append(k)
        name1.append('%s' % (data[k]['name']+' '+data[k]['title']))
    return id1, name1

def parse_2(html):
    '''
    解析第二层页面内容
    :param html: 第二层页面的响应内容
    :return: 每个皮肤的对应id(构造最终皮肤地址)和名字
    '''
    dct = re.search('{"data".*}', html).group()
    dct = json.loads(dct)
    skins = dct['data']['skins']
    id2 = []
    name2 = []
    for i in skins:
        id2.append(i['id'])
        name2.append(i['name'])
    return id2, name2

def save(url,fp):
    '''
    保存图片
    :param url: 皮肤地址
    :param fp: 保存路径
    :return: None
    '''
    try:
        if not os.path.exists(fp):
            content = download_img(url)
            with open(fp, 'wb') as f:
                f.write(content)
                print(fp)
    except:
        if os.path.exists(fp):
            os.remove(fp)
        print('保存失败', fp)
        return save(url, fp)

def first_step():
    '''
    第一步
    :return: 每个英雄的英文名(构造下一级网页)和对应中文名
    '''
    start_url = 'https://lol.qq.com/web201310/js/herovideo.js'  # 所有英雄信息
    html = download(start_url)
    id1, name1 = parse_1(html)
    return id1, name1

def second_step(hero):
    '''
    第二步
    :param hero: 每个英雄英文名(构造对应英雄地址)
    :return: 每个皮肤的对应id(构造最终皮肤地址)和名字
    '''
    url = 'https://lol.qq.com/biz/hero/%s.js' % hero  # 每个英雄对应js
    html = download(url)
    id2, name2 = parse_2(html)
    return id2, name2

def third_step(id, name1, name2):
    '''
    第三步
    :param id: 皮肤id
    :param name1: 原画名字
    :param name2: 皮肤名字
    :return: None
    '''
    if not os.path.exists(name1):
        os.mkdir(name1)
    if name2 == 'default':
        name2 = name1
    if '/' in name2:
        name2 = name2.replace('/','')
    url_img = 'https://ossweb-img.qq.com/images/lol/web201310/skin/big%s.jpg' % id  # 最终图片地址
    fp = '{0}/{1}{2}'.format(name1, name2, '.jpg')
    save(url_img, fp)

def main():
    '''
    主程序
    :return: None
    '''
    id1, name1 = first_step()
    for i in range(len(id1)):
        id2, name2 = second_step(id1[i])
        for j in range(len(id2)):
            third_step(id2[j], name1[i], name2[j])

if __name__ == '__main__':
    main()

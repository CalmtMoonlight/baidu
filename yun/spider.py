#! /usr/bin/env python
# -*- coding:utf-8 -*-
import json
import re
import urllib
import requests
import logging

import sys

import time

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
                    filename="message.log",
                    filemode="w")

STOKEN=''


class Yun(object):
    def __init__(self, url_verify):
        self.STOKEN = STOKEN
        self.url_verify = url_verify
        self.first_url, self.verify = url_verify
        self.INIT_URL = ''
        self.str_pwd = 'pwd=%s&vcode=&vcode_str=' % self.verify
        self.conn = requests.session()
        self.conn.get('http://pan.baidu.com/')
        self.BAIDUID = requests.utils.dict_from_cookiejar(self.conn.cookies)['BAIDUID']
        self.cookie = 'STOKEN=%s; BAIDUID=%s; BIDUPSID=7C5A33AAE1F0544D744C5F730DC86DBE; PSTM=1485576851; BDRCVFR[8Xaq1jJhPm_]=mk3SLVN4HKm; PSINO=1; H_PS_PSSID=; PANWEB=1; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1485577063; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1485577063;'%(self.STOKEN,self.BAIDUID)
        self.BDCLND = ''


        self.BDUSS = 'ENOQVk3N1dtcG9iSzlmdmZ-SWZKTVYzTDlqYjFSV1JmbG9ka1BPWkUxQUMyTE5ZSVFBQUFBJCQAAAAAAAAAAAEAAADZ7awk18~UwtK51q7p5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJLjFgCS4xYW'
        self.BDSTOKEN = ''
        self.UK = ''
        self.SHAREID = ''
        self.PATH = ''
        self.Referer = ''

        self.cookieS = [
            'STOKEN=%s'%self.STOKEN,
            'BAIDUID=%s' %self.BAIDUID,
            'BDCLND=%s' %self.BDCLND,
            'BIDUPSID=7C5A33AAE1F0544D744C5F730DC86DBE',
            'PSTM=1485576851',
            'BDRCVFR[8Xaq1jJhPm_]=mk3SLVN4HKm',
            'PSINO=1',
            'H_PS_PSSID=',
            'PANWEB=1',
            'Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1485577063',
            'Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1485577063',
        ]
        self.headers = {
            "Host": "pan.baidu.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;zh-CN,zh;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Origin": "http://pan.baidu.com",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": ";".join(self.cookieS),
            "Referer": "".join([self.INIT_URL])
        }

        self.verify_header = {
            "Host": "pan.baidu.com",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Origin": "http://pan.baidu.com",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.0.1471.813 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8"
        }

        self.SERVER_TIME = ''

        self.item_dict = {}


        self.first_url = self.deal_url(self.first_url)           # https://pan.baidu.com/s/1pLCQkQn
        self.url_post_verify = 'http://pan.baidu.com/share/verify?shareid=%s&uk=%s&t=%s&bdstoken=null&channel=chunlei&clienttype=0&web=1&app_id=250528&logid=MTQ4NTU3NzI0NDU2MzAuNzM0MDM2ODAwODQyOTE4Ng=='

        self.get_first_item()
        self.share_link_item()


    def deal_url(self,url):
        https,tail = url.split(':')
        if "http"==https:https='https'

        return ':'.join([https, tail])

    def get_first_item(self):
        req = requests.get(self.first_url, headers=self.headers)
        self.INIT_URL = req.url  # https://pan.baidu.com/share/init?shareid=51338524&uk=2268281588
        req = requests.get(self.INIT_URL,headers=self.headers)
        html = req.content

        self.SERVER_TIME = re.findall("\('SERVERTIME',(.*?)\)", html)[0].strip()
        self.SHAREID, self.UK = re.search("https://pan.baidu.com/share/init\?shareid=(\d*?)&uk=(\d*?)$", self.INIT_URL).groups()

        logging.info('加载验证码页面【成功】!')

    def _verify(self):
        """
        需要 【Referer】 信息
        :return:
        """
        url_post = self.url_post_verify %(self.SHAREID,self.UK,self.SERVER_TIME)

        self.verify_header['Referer'] = self.INIT_URL
        self.verify_header['Cookie'] = self.cookie

        req = requests.post(url=url_post, headers=self.verify_header, data=self.str_pwd)
        self.BDCLND = requests.utils.dict_from_cookiejar(req.cookies)["BDCLND"]
        self.cookie += '; BDCLND=%s' % self.BDCLND
        errno = json.loads(req.content)['errno']

        if errno == 0 and self.BDCLND !=None or '':
            logging.info('验证码输入【正确】')
            return True
        logging.error('验证码输入【错误】')
        print '验证码输入【错误】'
        return False

    def share_link_item(self):
        if not self._verify():
            return
        temp_link = 'https://pan.baidu.com/share/link?shareid=%s&uk=%s'%(self.SHAREID,self.UK)

        self.verify_header['Cookie'] = self.cookie
        req = requests.get(temp_link,headers=self.verify_header)
        html = req.content

        items = re.findall("yunData.setData\((.*?)\);", html)

        logging.info('加载分享页面【成功】')
        item_data = json.loads(items[0], encoding='utf8')
        list_info = item_data["file_list"]['list'][0]

        self.BDSTOKEN = item_data["bdstoken"]
        self.PATH = list_info['path']


    def save(self, target_path='/test'):

        self.__save(self.SHAREID, self.UK, self.BDSTOKEN, self.BDUSS, self.STOKEN, self.BDCLND, self.first_url,self.PATH,target_path)

    def __save(self, shareid, uk, bdstoken, bduss, stoken, bdclnd, refer_url, filelists, target_path='/'):
        time.sleep(1)
        _headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'BDUSS=%s;STOKEN=%s;BDCLND=%s' % (bduss, stoken, bdclnd),
            'DNT': '1',
            'Referer': refer_url,
            'Host': 'yun.baidu.com',
            "Origin": "http://pan.baidu.com",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        _filelist = '["%s"]' % (
            urllib.unquote(str(filelists)).decode('utf-8').encode('utf8'))
        _payload = {
            'filelist': _filelist,
            'path': target_path,
        }
        _temp_url = "https://pan.baidu.com/share/transfer?shareid=%s&from=%s&bdstoken=%s&channel=chunlei&web=1&app_id=250528&logid=MTQ4NTYxMDcyNzkwMzAuNjE5NzA4NjA5OTIwODQyOQ==&clienttype=0" % (
        shareid, uk, bdstoken)
        r = requests.post(_temp_url, headers=_headers, data=_payload)
        html = r.content
        # print html
        message = ""
        if '"errno":12' in html:
            message = "file exit!"
            print message
        elif '"errno":0' in html:
            message = "success!"
            print message

        else:

            if '"errno":-6' in html:
                message = 'stoken expire 请更换STOKEN!'
            elif '"errno":-9' in html:
                message = "【BDCLND】 error"
            elif '"errno":1' in html:
                message = "【BDUSS】 error"
            elif '"errno":2' in html:
                message =  "【_payload 】格式错误! or 路径不存在！"
        logging.info(self.url_verify)
        logging.info(message+"\n"*2+"*"*80)


if __name__ == '__main__':

    # STOKEN = open("token").read().strip()
    # print STOKEN


    urls = [
        ('https://pan.baidu.com/s/1pLCQkQn', '89yi'),
        ("https://pan.baidu.com/s/1o8lNEkU", 'tthx'),
    ]

    yun = Yun(urls[0])          #传入元组
    yun.save("/test")           #网盘路径必须存在
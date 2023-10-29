# login.py
import json
import time
import requests
import re
import os
import sys
import urllib.parse

from encryption import srun_base64, srun_md5, srun_sha1, srun_xencode

loginURL = ''
enc = 's' + 'run' + '_bx1'
n = 200
type_num = 1
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69'}


def readConfig():
    global loginInfo, loginURL, header, device, os
    configFile = open(os.path.join(
        os.path.dirname(sys.argv[0]), 'config.json'))
    configInfo = json.loads(str(configFile.read()))
    loginInfo = configInfo['userInfo']
    loginURL = configInfo['platformInfo']['loginURL']
    device = configInfo['platformInfo']['device']
    os = configInfo['platformInfo']['os']


def getInfo():
    resp = requests.get(loginURL)
    current_url = resp.url
    resp_info = dict(urllib.parse.parse_qsl(
        urllib.parse.urlsplit(current_url).query))
    loginInfo['ac_id'] = resp_info['ac_id']
    loginInfo['double_stack'] = 0
    loginInfo['otp'] = False
    resp_context_lines = resp.text.splitlines()
    resp_ip = resp_context_lines[109]
    pattern = r'ip\s+:\s+"(\d+\.\d+\.\d+\.\d+)"'
    ip_match = re.search(pattern, resp_ip)
    loginInfo['ip'] = ip_match.group(1)


def getChallenge(data):
    return requests.get(loginURL + '/cgi-bin/get_challenge', params=data, headers=header)


def getPortal(data):
    return requests.get(loginURL + '/cgi-bin/srun_portal', params=data, headers=header)


def info(d, k):
    return '{SRBX1}' + srun_base64.get_base64(srun_xencode.get_xencode(json.dumps(d), k))


def login():
    try:
        baidu_resp = requests.get("https://baidu.com", timeout=5)
        if baidu_resp.status_code == 200:
            print('Network available. Exited.')
            return
    except:
        print('Network unavailable. Connecting...')
    if (bool(loginInfo['domain'])):
        username = loginInfo['username'] + '@' + loginInfo['domain']
    else:
        username = loginInfo['username']
    ip = loginInfo['ip']
    get_challenge_params = {
        "callback": "jQuery112407291255008282638_"+str(int(time.time()*1000)),
        "username": username,
        "ip": ip,
        "_": int(time.time()*1000),
    }
    token_resp = getChallenge(get_challenge_params)
    token = re.search('"challenge":"(.*?)"', token_resp.text).group(1)
    payload = {
        'username': username,
        'password': loginInfo['password'],
        'ip': loginInfo['ip'],
        'acid': loginInfo['ac_id'],
        'enc_ver': enc
    }
    encoded_payload = info(payload, token)
    hmd5 = srun_md5.get_md5(loginInfo['password'], token)
    chkstr = token + username
    chkstr += token + str(hmd5)
    chkstr += token + loginInfo['ac_id']
    chkstr += token + loginInfo['ip']
    chkstr += token + str(n)
    chkstr += token + str(type_num)
    chkstr += token + encoded_payload
    loginInfo['password'] = '{MD5}' + hmd5

    params = {
        'callback': 'jQuery112407291255008282638_'+str(int(time.time()*1000)),
        'action': 'login',
        'username': username,
        'password': loginInfo['password'],
        'ac_id': loginInfo['ac_id'],
        'ip': loginInfo['ip'],
        'chksum': srun_sha1.get_sha1(chkstr),
        'info': encoded_payload,
        'n': n,
        'type': type_num,
        'os': os,
        'name': device,
        'double_stack': 0
    }
    resp = getPortal(params)
    print(resp.text)


def main():
    readConfig()
    getInfo()
    login()


if __name__ == '__main__':
    main()

import requests
from bs4 import BeautifulSoup as bs4
import re
import json
from pprint import pprint
from datetime import datetime, timezone
from dateutil import tz
import os
import errno
import pytz
from selenium import webdriver
import time
import random

def get_photo(url, num):
    html = request.get()

def login():
    chromedriver = '/usr/local/bin/chromedriver'
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    options.add_argument('chromever="73.0.3683.68"')
    browser = webdriver.Chrome(chromedriver, options=options)
    login_url = 'https://www.instagram.com/accounts/login/'
    browser.get(login_url)
    time.sleep(3)
    username = browser.find_element_by_name("username")
    password = browser.find_element_by_name("password")

    with open("/Users/Nicholas/GitHub/credentials/instagram.json", "r") as file:
          login = json.load(file)
    if isinstance(login, list):
        login = random.choice(login)

    username.send_keys(login['username'])
    password.send_keys(login['password'])
    login_attempt = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')

    login_attempt.click()
    time.sleep(2)
    s = requests.session()

    human_headers = { "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "accept-language" : "en-US,en;q=0.9",
                        "accept-encoding" : "gzip, deflate, br",
                        "upgrade-insecure-requests" : "1",
                        "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.183 Safari/537.36 Vivaldi/1.96.1147.64"
                    }
    s.headers.update(human_headers)

    for cookie in browser.get_cookies():
        c = {cookie['name']: cookie['value']}
        s.cookies.update(c)
    time.sleep(2)
    return browser, s
    

def get_photos(url, browser, s):
    browser.get(url)
    time.sleep(2)
    html = browser.page_source
    # browser.quit()
    soup = bs4(html, 'html.parser')
    # print(soup.prettify())
    try:
        for x in soup.findAll('script', type='text/javascript'):
            if 'shortcode' in ''.join(x.contents):
                # print('short')
                st = str(x.contents[0])
                st = re.sub(r'(window\._sharedData = )|;', '', st)
                d = json.loads(st)
            else:
                return
    except Exception as e:
        d = dict()

    if not d:
        return []
    # pprint(d)
    profile_img = d['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd']
    d = d['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
    jsons = []
    for x in d:
        contents = x['node']
        account = contents['owner']['username']
        page_id = contents['shortcode']

        base_path = f'./instagram/{account}/{page_id}'
        img_file = f'{base_path}.jpg'
        json_file = f'{base_path}.json'
        if os.path.exists(img_file) and os.path.exists(json_file):
            print(base_path)
            continue
        caption = contents['edge_media_to_caption']['edges'][0]['node']['text']
        if not contents['comments_disabled']:
            comments = contents['edge_media_to_comment']['count']
        else:
            comments = 0
        timestamp = contents['taken_at_timestamp']
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/Chicago')
        dt = datetime.utcfromtimestamp(contents['taken_at_timestamp'])
        dt = dt.replace(tzinfo=from_zone)
        dt = dt.astimezone(to_zone)
        dt = dt.strftime('%Y-%B-%d %H:%M:%S')

        img_url = contents['display_url']
        likes = contents['edge_liked_by']['count']

        # print('caption', caption)
        # print('page_id', page_id)
        # print('comments', comments)
        # print('likes', likes)
        # print('time', time)

        if not os.path.exists(os.path.dirname(img_file)):
            try:
                os.makedirs(os.path.dirname(img_file))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(img_file, "wb") as f:
            f.write(s.get(img_url, allow_redirects=True).content)

        with open(json_file, 'w') as f:
            my_json = {'profile_img':profile_img, 'caption':caption, 'page_id':page_id, 'comments':comments, 'likes':likes, 'time':dt, 'timestamp':timestamp, 'account':account, 'img_url':img_url}
            json.dump(my_json, f)
            jsons.append(my_json)
            # print(json)

    return jsons
    # for x in d2.keys():
    #     if 'https://scontent-sjc3-1.cdninstagram.com/vp/1bca4ee6dbd2999af2e44d61e02cf91c/5DFAA57A/t51.2885-19/s320x320/66473343_731529173935811_8097850297587597312_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com' in json.dumps(d2[x]):
    #         print(x)
    # return re.findall(r'(?<=shortcode":")[^"]*(?=")', html))

if __name__ == '__main__':
    browser, s = login()
    url = 'https://www.instagram.com/uwmadison/'
    get_photos(url, browser, s)
    browser.quit()
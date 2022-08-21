from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
born_date = os.environ['BORN_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['date'], weather['weather'], math.floor(weather['low']),math.floor(weather['high']),math.floor(weather['temp']), weather['wind'], weather['airQuality']

def get_count():
  delta_day = today - datetime.strptime(start_date, "%Y-%m-%d")
  survive_day = today - datetime.strptime(born_date, "%Y-%m-%d")
  return delta_day.days, survive_day.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("http://open.iciba.com/dsapi/")
  return words.json()['content'], words.json()['note']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
date, wea, low, high, temperature, wind, airquality = get_weather()
love_days, survive_days = get_count()
content, note = get_words()
data = {"date":{"value":date, "color":get_random_color()},"weather":{"value":wea, "color":get_random_color()},"low":{"value":low, "color":get_random_color()},"high":{"value":high, "color":get_random_color()},"temperature":{"value":temperature, "color":get_random_color()},"wind":{"value":wind, "color":get_random_color()},"airquality":{"value":airquality, "color":get_random_color()},"survive_days":{"value":survive_days, "color":get_random_color()},"love_days":{"value":love_days, "color":get_random_color()},"birthday_left":{"value":get_birthday(), "color":get_random_color()},"content":{"value":content, "color":get_random_color()},"note":{"value":note, "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)

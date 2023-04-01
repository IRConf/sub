import requests
import re
import pybase64
import urllib.parse

def translate(text):
  replacements = {
      "MCI" : "همراه‌اول",
      "MTN" : "ایرانسل",
      "RTL" : "رایتل",
      "MKH" : "مخابرات",
      "HWB" : "های‌وب",
      "AST" : "آسیاتک",
      "SHT" : "شاتل",
      "PRS" : "پارس‌آنلاین",
      "MBT" : "مبین‌نت",
      "ASK" : "اندیشه‌سبز",
      "RSP" : "رسپینا",
      "AFN" : "افرانت",
      "ZTL" : "زی‌تل",
      "PSM" : "پیشگامان",
      "ARX" : "آراکس",
      "SMT" : "سامانتل",
      "FNV" : "فن‌آوا",
      "APT" : "آپتل"
      }

  for old, new in replacements.items():
      text = text.replace(old, new)

  return text


domains = requests.get('https://ircf.space/export.php').text

configs = requests.get('https://raw.githubusercontent.com/IranianCypherpunks/sub/main/config').text

for domain in domains.splitlines():
  name = domain.split("\t\t")[1]
  name = translate(name)
  domain = domain.split("\t\t")[0]
    
  for conf in configs.splitlines():
    if conf.startswith('vless://'):
      conf = re.sub(r"@([^:]+):", "@" + domain + ":", conf)
      conf = re.sub(r"#(.*)$", "#" + urllib.parse.quote_plus(name) + " Iranian Cypherpunks", conf)
      print(conf)
    elif conf.startswith('vmess://'):
      conf = conf.replace('vmess://', '')
      conf = pybase64.urlsafe_b64decode(conf).decode('utf-8')
      conf = re.sub(r"\"add\":\"([^\"]+)\"", '"add":"' + domain + '"', conf)
      conf = re.sub(r"\"ps\":\"([^\"]+)\"", '"ps":"' + name + ' Iranian Cypherpunks"', conf)
      conf = conf.encode()
      conf = 'vmess://' + pybase64.urlsafe_b64encode(conf).decode('utf-8')
      print(conf)

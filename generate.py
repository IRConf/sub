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
      "APT" : "آپتل",
      "DBN" : "دیده‌بان‌نت",
      "SHM" : "شاتل‌موبایل"
      }

  for old, new in replacements.items():
      text = text.replace(old, new)

  return text


domains_fallback = """mci.ircf.space		MCI
mcix.ircf.space		MCI
mcic.ircf.space		MCI
mtn.ircf.space		MTN
mtnx.ircf.space		MTN
mtnc.ircf.space		MTN
mkh.ircf.space		MKH
mkhx.ircf.space		MKH
rtl.ircf.space		RTL
hwb.ircf.space		HWB
ast.ircf.space		AST
sht.ircf.space		SHT
prs.ircf.space		PRS
mbt.ircf.space		MBT
ask.ircf.space		ASK
rsp.ircf.space		RSP
afn.ircf.space		AFN
ztl.ircf.space		ZTL
psm.ircf.space		PSM
arx.ircf.space		ARX
smt.ircf.space		SMT
shm.ircf.space		SHM
fnv.ircf.space		FNV
dbn.ircf.space		DBN
apt.ircf.space		APT
fnp.ircf.space		FNP
ryn.ircf.space		RYN
"""

#domains = requests.get('https://ircf.space/export.php').text

#if not domains:
#  domains = domains_fallback

domains = domains_fallback

configs = requests.get('https://raw.githubusercontent.com/IranianCypherpunks/sub/main/config').text

print(configs)

for domain in domains.splitlines():
  name = domain.split("\t\t")[1]
  name = translate(name)
  domain = domain.split("\t\t")[0]
    
  for conf in configs.splitlines():
    if conf.startswith('vless://'):
      conf = re.sub(r"@([^:]+):", "@" + urllib.parse.quote(domain) + ":", conf)
      conf = re.sub(r"#(.*)$", "#" + urllib.parse.quote(name + " Iranian Cypherpunks"), conf)
      print(conf)
    elif conf.startswith('vmess://'):
      conf = conf.replace('vmess://', '')
      conf = pybase64.urlsafe_b64decode(conf).decode('utf-8')
      conf = re.sub(r"\"add\":\"([^\"]+)\"", '"add":"' + domain + '"', conf)
      conf = re.sub(r"\"ps\":\"([^\"]+)\"", '"ps":"' + name + ' Iranian Cypherpunks"', conf)
      conf = conf.encode()
      conf = 'vmess://' + pybase64.urlsafe_b64encode(conf).decode('utf-8')
      print(conf)

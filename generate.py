import requests
import re
import pybase64

domains = requests.get('https://ircf.space/export.php').text

configs = requests.get('https://raw.githubusercontent.com/IranianCypherpunks/sub/main/config').text

for domain in domains.splitlines():
  name = domain.split("\t\t")[1]
  domain = domain.split("\t\t")[0]
    
  for conf in configs.splitlines():
    if conf.startswith('vless://'):
      conf = re.sub(r"@([^:]+):", "@" + domain + ":", conf)
      conf = re.sub(r"#(.*)$", "#" + name + " Iranian Cypherpunks", conf)
      print(conf)
    elif conf.startswith('vmess://'):
      conf = conf.replace('vmess://', '')
      conf = pybase64.urlsafe_b64decode(conf).decode('utf-8')
      conf = re.sub(r"\"add\":\"([^\"]+)\"", '"add":"' + domain + '"', conf)
      conf = re.sub(r"\"ps\":\"([^\"]+)\"", '"ps":"' + name + ' Iranian Cypherpunks"', conf)
      conf = conf.encode()
      conf = 'vmess://' + pybase64.urlsafe_b64encode(conf).decode('utf-8')
      print(conf)

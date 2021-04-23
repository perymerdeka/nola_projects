import requests
import random
from bs4 import BeautifulSoup

# getting proxy
def get_proxy():
    proxies = []
    with open('Webshare_10_proxies.txt', 'r') as proxy:
        for prox in proxy:
            spl_prox = prox.split(':')

            # create proxy dict
            prox_dict = {
                'username': spl_prox[2],
                'password': spl_prox[3].replace('\n', ''),
                'ip':spl_prox[0],
                'port':spl_prox[1],

            }
            # setting proxy
            set_proxy = prox_dict['username'] + ':' + prox_dict['password'] + '@' + prox_dict['ip'] + ':' + prox_dict['port']

            # append to list
            proxies.append(set_proxy)
        print(proxies)

        return random.choice(proxies)



url = "https://www.realtor.com/realestateandhomes-detail/4380-Vireo-Ave-Apt-5F_Bronx_NY_10470_M41068-69696"
res = requests.get(url)

f = open('res.html', 'w+')
f.write(res.text)
f.close()

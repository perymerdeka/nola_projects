import requests
import json
from bs4 import BeautifulSoup

# headers
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'cache-control':'max-age=0',
    # 'cookie':'zguid=23|%2482971312-d59b-4dbf-95e6-be130386df47; zgsession=1|5a99c9d4-4d68-4926-8ad9-645ef59232d3; _ga=GA1.2.1911770309.1609684744; _gid=GA1.2.567505807.1609684744; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; zjs_user_id=null; zjs_anonymous_id=%2282971312-d59b-4dbf-95e6-be130386df47%22; _gcl_au=1.1.432493643.1609684746; KruxPixel=true; DoubleClickSession=true; _pxvid=6e6f9ed3-4dd1-11eb-a0fb-0242ac12000e; _pin_unauth=dWlkPVpHUXlNR1JoTkRNdFpqUmlNUzAwT1dSa0xXSXpOMll0TjJJd05ESXdOV1ptTkRFdw; KruxAddition=true; g_state={"i_p":1609694581605,"i_l":1}; JSESSIONID=58F1189F61A4E62830C9E1577A776160; _px3=f7c3f9a333c148cb851665258ec4b7589cdc6db6b40183560c794a50097773ab:YQWzRQ3YL9ybVCojGYRFeEVm2CuOUepLnLgS8rxRLlb2JLJEy9DR7m5oVclE8ZWuwgIitoxFTAtaA3tMyA6/8A==:1000:WkYVEE+mCK+jlGnca7AJU9f49kQHr/dQx8h0ATyLNpFRW5k622JQK56sbVDbmQmgNXUcDlfWuH7ZjBvBSraH1T4Tc6WWXMNp9z+nhxODOlH7qAPF/d2O545/PxzCrWnON9y4eBftj0wc6whJLlxJgFqcG6vvcUDcbdaJ7i0YNCo=; _uetsid=6ee457b04dd111eba15027b6e0f16ac3; _uetvid=6ee4a5704dd111eb81fb1b375ee4179a; ki_r=; _gat=1; search=6|1612344715732%7Crect%3D41.2150938491687%252C-73.1429955625%252C40.1927894141644%252C-74.8129174375%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%096181%09%09%09%09%09%09; ki_s=; AWSALB=lHPoabWbXYbNGvKvYt1gxXP4nbu1VVgjApd8xBy4QV69bNnQFyo1zIS9OcZP3OGY3Yj//v+Lo0L9gaEm7Mc78Ebd7Ocb/00Z0l2Er7+nAk8ryv9gdjLhArC4SC1g; AWSALBCORS=lHPoabWbXYbNGvKvYt1gxXP4nbu1VVgjApd8xBy4QV69bNnQFyo1zIS9OcZP3OGY3Yj//v+Lo0L9gaEm7Mc78Ebd7Ocb/00Z0l2Er7+nAk8ryv9gdjLhArC4SC1g; ki_t=1609752622273%3B1609752622273%3B1609752727193%3B1%3B7',
    'sec-ch-ua':'"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    'sec-ch-ua-mobile':'?0',
    'sec-fetch-dest':'empty',
    'sec-fetch-mode':'cors',
    'sec-fetch-site':'same-origin',
    'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
# params
params = {
    'searchQueryState':'{"pagination":{},"usersSearchTerm":"New York, NY","mapBounds":{"west":-74.8129174375,"east":-73.1429955625,"south":40.42945465007956,"north":40.98120890098652},"regionSelection":[{"regionId":6181,"regionType":6}],"isMapVisible":true,"filterState":{"sortSelection":{"value":"globalrelevanceex"},"isAllHomes":{"value":true}},"isListVisible":true,"mapZoom":9}',
    'wants':'{"cat1":["listResults","mapResults"]}',
    'requestId':'4'
}


url = 'https://www.zillow.com/homes/Atlanta,-KS_rb/'
res = requests.get(url,params=params ,headers=headers)
f = open('res.html', 'w+')
f.write(res.text)
f.close()

soup = BeautifulSoup(res.text, 'html.parser')

# scraping process
container = soup.find('ul', attrs={'class':'photo-cards photo-cards_wow photo-cards_short'})
for card in container.contents:
    script = card.find('script', attrs={'type':'application/ld+json'})
    if script:
        script_parser = script.contents[0]
        data_json = json.loads(script_parser)
        print(data_json)
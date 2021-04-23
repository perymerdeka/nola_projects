import requests
import os
from bs4 import BeautifulSoup



class RedfinScraper:
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
        'cache-control': 'max-age=0',
        # 'cookie': 'RF_BROWSER_ID=yPWZHmWXScOzUJRQtJGFWw; RF_BID_UPDATED=1; RF_BROWSER_CAPABILITIES=%7B%22screen-size%22%3A4%2C%22ie-browser%22%3Afalse%2C%22events-touch%22%3Afalse%2C%22ios-app-store%22%3Afalse%2C%22google-play-store%22%3Afalse%2C%22ios-web-view%22%3Afalse%2C%22android-web-view%22%3Afalse%7D; _gcl_au=1.1.250143412.1610111234; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; G_ENABLED_IDPS=google; _ga=GA1.2.1628291100.1610111237; _gaexp=GAX1.2.vBpOFG-PTEe30DWBrV8-3A.18708.1; RF_VISITED=true; RF_CORVAIR_LAST_VERSION=349.0.1; AKA_A2=A; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.1707398762.1610510328; FEED_COUNT=0%3Af; unifiedLastSearch=name%3DNew%2520York%26subName%3DNew%2520York%252C%2520NY%252C%2520USA%26url%3D%252Fcity%252F30749%252FNY%252FNew-York%26id%3D2_30749%26type%3D2%26unifiedSearchType%3D2%26isSavedSearch%3D%26countryCode%3DUS; _uetsid=a2ca4730555311eb89968562b7527a0c; _uetvid=6e67fda051b211eb8c049745a158b017; userPreferences=parcels%3Dtrue%26schools%3Dfalse%26mapStyle%3Ds%26statistics%3Dtrue%26agcTooltip%3Dfalse%26agentReset%3Dfalse%26ldpRegister%3Dfalse%26afCard%3D2%26schoolType%3D0%26viewedSwipeableHomeCardsDate%3D1610510341614; RF_MARKET=newyork; RF_LAST_SEARCHED_CITY=Elmont; g_state={"i_p":1610517618689,"i_l":1}',
        'referer': 'https://www.redfin.com/city/30749/NY/New-York',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }

    def get_response(self, url):
        res = requests.get(url, headers=self.headers)

        try:
            print('creating directory to append temporary file')
            os.makedirs('redfin_com_temporary')
        except FileExistsError:
            print('directory created')

        # create response temporary file
        f = open('redfin_com_temporary/res.html', 'w+')
        f.write(res.text)
        f.close()

        # status code
        print(f'Site Status Code: {res.status_code}')
        return res

    def get_total_pages(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        page_text = soup.find('span',
                              attrs={'class': 'pageText', 'data-rf-test-name': 'download-and-save-page-number-text'}).text.strip()
        total_page = int(page_text.split('of')[1])
        print('Total Page Found: {}'.format(total_page))
        return total_page

    def get_all_url(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        container_flex_wrap = soup.find_all('div', attrs={'class':'flex flex-wrap'})
        print(container_flex_wrap)

    def run(self):
        url = 'https://www.redfin.com/city/30749/NY/New-York'
        res = self.get_response(url=url)
        self.get_total_pages(response=res.text)


if __name__ == '__main__':
    redfin_scraper = RedfinScraper()
    redfin_scraper.run()

import time
from requests_html import HTMLSession, AsyncHTMLSession
from bs4 import BeautifulSoup

class RealtorTester:
    # base url
    base_url = 'https://www.realtor.com'
    # ansync requests
    asession = AsyncHTMLSession()

    # getting requests
    session = HTMLSession()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
        'cache-control': 'max-age=0',
        # 'cookie': 'split=n; split_tcv=111; __vst=a952cf94-74f0-4477-a8dd-142573636bd5; __ssn=fefe8240-a766-4fca-9003-dcca5c2ae55a; __ssnstarttime=1609688060; __split=70; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; ab.storage.userId.7cc9d032-9d6d-44cf-a8f5-d276489af322=%7B%22g%22%3A%22visitor_a952cf94-74f0-4477-a8dd-142573636bd5%22%2C%22c%22%3A1609688066087%2C%22l%22%3A1609688066087%7D; ab.storage.deviceId.7cc9d032-9d6d-44cf-a8f5-d276489af322=%7B%22g%22%3A%22bd05ae26-523f-cf34-391e-69acfbbd1121%22%2C%22c%22%3A1609688066094%2C%22l%22%3A1609688066094%7D; AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1; ajs_anonymous_id=%2298c8687f-4011-4721-b24c-aa97d39c89a7%22; s_ecid=MCMID%7C09142292949000337642279608827887032169; _tac=false~self|not-available; _ta=us~1~89df68bc35032d48c293adce8574aa42; AMCVS_AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=1; G_ENABLED_IDPS=google; _ga=GA1.2.73478017.1609688063; _ncg_id_=9e9a5521-ca51-4b89-a7db-3227f2360c46; __qca=P0-1293245987-1609688071782; user_activity=return; _gid=GA1.2.1148966151.1609918526; _ncg_g_id_=b65a1694-2043-4c71-a68e-f8270f7ba0bb; g_state={"i_p":1610011930458,"i_l":2}; reese84=3:e1K9XiyZyQ1TuW9cA+7khw==:ms1e8Y4FZYJQA/Bk2IZeqFWmNTCJkeo917N4dDeCzvXgOcn1CBu5vu5aODSvSqrlNKBJJP81tuBY4SIBxesWyk7cWHAi7IpT5s4Q1gVWeqQN7dJ66cWC2zlM//ePRwJDS6JdR5vfT1auGRH4DSZfobVSxbm4JGtO5uyUVPkepDaVrtQHxRHz7QbL8dyIWv7n+E5T+H68WterXRi4+px+sEwSGEvOplWtLyZ+cVFZ5fvofrJryvNwxfuGeYjwwW3DJWncT34+6j7M08skDCmVPoqWfd2pIsvmLY0sT+AFEqncxgx86I7ITCgHmxRPz7pHEYAalGvUfGOZf0gI01H0Ukae7vVA+M1HFWNvcgo1/agF4Ju2OFvFybuuBHB4T0m2vhJT4oWadvm3MPhAaFqE9oKu+AmvwhjSqzclPnEPkV4=:HeJlpTzg/15fARVoZ23VV+fpc462D19UIBPSIV+dsAE=; AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-637568504%7CMCIDTS%7C18634%7CMCMID%7C09142292949000337642279608827887032169%7CMCAAMLH-1610542569%7C3%7CMCAAMB-1610542569%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1609944969s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.1.1; _tas=iqdtr0htaxr; AMCV_AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-637568504%7CMCMID%7C09142292949000337642279608827887032169%7CMCIDTS%7C18634%7CMCOPTOUT-1609944974s%7CNONE%7CvVersion%7C5.1.1; adcloud={%22_les_v%22:%22y%2Crealtor.com%2C1609939574%22}; QSI_HistorySession=https%3A%2F%2Fwww.realtor.com%2F~1609688070308%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FNew-York_NY~1609918526474%7Chttps%3A%2F%2Fwww.realtor.com%2F~1609937775177; _ncg_sp_ses.cc72=*; _ppl_visit=uuid=7868f1d2-3df1-4abe-b3f9-733053aa6005; _ppl_visitor=uuid=186d57ec-af42-4aa8-8a55-31f1a636760e&birth=1609688072&count=4; srchID=4773e3e0d0b040849e28245665f5892a; _uetsid=be54dde04ff111ebb07cd52894390ee3; _uetvid=2c3fa0004dd911ebaec4f16407b730ff; criteria=pg%3D1%26locSlug%3DNew-York_NY%26sprefix%3D%252Frealestateandhomes-search%26city%3DNew%2520York%26state_code%3DNY%26state_id%3DNY%26area_type%3Dcity%26search_type%3Dcity%26lat%3D40.6634682%26long%3D-73.9386968%26county_fips%3D36081%26county_fips_multi%3D36081-36047-36085-36005-36061%26loc%3DNew%2520York%252C%2520NY; last_ran=1609937782652; last_ran_threshold=1609937782653; ab.storage.sessionId.7cc9d032-9d6d-44cf-a8f5-d276489af322=%7B%22g%22%3A%2232091e73-f624-6c6e-d5b4-aa23febd0bba%22%2C%22e%22%3A1609939582726%2C%22c%22%3A1609937782730%2C%22l%22%3A1609937782730%7D; _ncg_sp_id.cc72=9e9a5521-ca51-4b89-a7db-3227f2360c46.1609688072.1.1609937785.1609688072.363410b8-664b-41d7-b70f-189ebe1fcbd3',
        'if-none-match': '"166bc1-yPUgYUcwf2+/wXOVrfBasoAyFus"',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    # func to handle response
    def get_response(self, url):
        res = self.session.get(url, headers=self.headers)
        f = open('res.html', 'w+')
        f.write(res.text)
        f.close()
        print(f'Response Status Code: {res.status_code}')
        with open('res.html', 'r') as bot_checker:
            soup = BeautifulSoup(bot_checker, 'html.parser')
            title = soup.find('title')
            try:
                bot_params = "Pardon Our Interruption"
                if title.text.strip() == bot_params:
                    print('Captcha detected')
                    print('Rendering Javacript')
                    rendering_response = self.session.get(url, headers=self.headers)
                    return rendering_response

                return res

            except TypeError:
                print('sleeping 10 second')
                time.sleep(10)
                return res

    def get_url(self, response):
        pass


    def run(self):
        url = 'https://www.realtor.com/realestateandhomes-search/New-York_NY'
        res = self.get_response(url)


if __name__ == '__main__':
    tester = RealtorTester()
    tester.run()
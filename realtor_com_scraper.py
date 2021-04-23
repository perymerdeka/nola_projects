import json
import random
import re
import os
import time
import backoff
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class RealtorScraper:
    # base url
    base_url = 'https://www.realtor.com'

    # add render support
    splash_url = 'http://localhost:8050/render.html'
    final_data = []
    session = requests.Session()

    # selenium driver PATH
    PATH = os.path.join(os.path.abspath(os.curdir), 'driver/chromedriver')
    use_selenium = True

    # backoff exception
    retry_timeout = backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException
        ),
        max_tries=10
    )

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

    # getting proxy
    def get_proxy(self):
        proxies = []
        with open('proxy/Webshare_10_proxies.txt', 'r') as proxy:
            for prox in proxy:
                spl_prox = prox.split(':')

                # create proxy dict
                prox_dict = {
                    'username': spl_prox[2],
                    'password': spl_prox[3].replace('\n', ''),
                    'ip': spl_prox[0],
                    'port': spl_prox[1],

                }

                # set proxy
                set_proxy = 'http://' + prox_dict['username'] + ':' + prox_dict['password'] + '@' + prox_dict[
                    'ip'] + ':' + prox_dict['port']
                # append to list
                proxies.append(set_proxy)

        return random.choice(proxies)

    @retry_timeout
    def get_response(self, url):
        # create directory to append temporary file
        try:
            os.makedirs('realtor_temporary')

        except FileExistsError:
            pass

        res = requests.get(url, headers=self.headers)
        f = open('realtor_temporary/res.html', 'w+')
        f.write(res.text)
        f.close()
        print(f'Response Status Code: {res.status_code}')

        # bot bypass
        bypass_params = 'Pardon Our Interruption'
        with open('realtor_temporary/res.html', 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
            title = soup.find('title').text.strip()
            if title == bypass_params:
                proxies = {
                    'http': self.get_proxy()
                }

                print('Requests Blocked, try using Proxy...')
                print(f'Use Proxy: {self.get_proxy()}')
                res_prox = requests.get(url, proxies=proxies)
                print('Web Status Code with Proxy: {}'.format(res_prox.status_code))
                if res_prox.status_code == 405:
                    print('Proxy Blocked Using Selenium...')
                    if self.use_selenium:
                        driver = webdriver.Chrome(self.PATH)
                        driver.get(url)

                        # file writing
                        print('Getting Content (using selenium) {}'.format(url))
                        f = open('realtor_temporary/res.html', 'w')
                        f.write(driver.page_source)
                        f.close()

                        # bot cheking
                        with open('realtor_temporary/res.html', 'r') as files:
                            soup_parse = BeautifulSoup(files, 'html.parser')
                            title = soup_parse.find('title').text.strip()

                            if title == bypass_params:
                                print('Selenium Requests Blocked, wait 30 seconds')
                                time.sleep(30)

                        return driver.page_source

            else:
                self.use_selenium = False
                print('Selenium Status: {}'.format(self.use_selenium))
                return res

    # getting total pages
    pages = []

    def get_total_pages(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        paginations = soup.find('div', attrs={'data-testid': 'pagination'}).find_all('a')
        for paginate in paginations:
            self.pages.append(paginate.get_text())

        total_pages = int(self.pages[6])
        return total_pages

    # get all url on page
    results = []  # <- storing result

    def get_all_url(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        container = soup.find('ul', attrs={'data-testid': 'property-list-container'})
        property_list = container.find_all('li', attrs={'data-testid': 'result-card'})
        for prop in property_list:
            try:
                address = prop.find('div', attrs={'data-label': 'pc-address',
                                                  'class': 'jsx-4195823209 address ellipsis'}).text.strip()
            except:
                address = prop.find('div', attrs={'data-label': 'pc-address', 'class': 'address'}).text.strip()

            link = self.base_url + prop.find('a')['href']

            self.results.append(
                {
                    'address': address,
                    'url': link
                }
            )
        print(f'Total URL Found: {len(self.results)}')
        return self.results

    @retry_timeout
    def get_detail(self, dict_url_list):

        """ getting url result"""
        global driver
        with open('realtor_temporary/result.json', 'w+') as file:
            json.dump(dict_url_list, file)

        print('URL Json Created')

        # error handler

        # dev mode
        start = int(input("Getting Detail Start From: "))
        dict_url_list = dict_url_list[start:23]

        for id, data in enumerate(dict_url_list):
            print('Processing {} of {} URL:{}'.format(id+1, len(dict_url_list),  data['url']))
            if self.use_selenium:
                print("Selenium Status {}".format(self.use_selenium))
                driver = webdriver.Chrome(self.PATH)
                driver.get(data['url'])
                f = open('realtor_temporary/res_detail.html', 'w+')
                f.write(driver.page_source)
                f.close()

                # parsing content
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # bot cheking
                with open('realtor_temporary/res_detail.html', 'r') as files:
                    soup_parser = BeautifulSoup(files, 'html.parser')
                    title_parser = soup_parser.find('title').text.strip()
                    bypass_params = 'Pardon Our Interruption'
                    if title_parser == bypass_params:
                        print('Selenium Requests Blocked, wait 30 seconds')
                        time.sleep(30)

            else:
                self.use_selenium = False
                print('Selenium status {}'.format(self.use_selenium))
                print('using requests..')

                res = requests.get(data['url'], headers=self.headers)
                print('Parsing Content..')
                soup = BeautifulSoup(res.text, 'html.parser')
                f = open('realtor_temporary/res_detail.html', 'w+')
                f.write(res.text)
                f.close()
                with open('realtor_temporary/res_detail.html', 'r') as files:
                    soup_parser = BeautifulSoup(files, 'html.parser')
                    title_parser = soup_parser.find('title').text.strip()
                    bypass_params = 'Pardon Our Interruption'
                    if title_parser == bypass_params:
                        print('Requests Blocked Using selenium to Getting detail')
                        soup = BeautifulSoup(driver.page_source)

            # scraping process
            try:
                price = soup.find('div', attrs={'data-testid': 'price-section'}).find('span').text.strip()
            except AttributeError:
                price = soup.find('span', attrs={'class': 'price'}).text.strip()

            try:
                owner_name = soup.find('span', attrs={'class': 'jsx-904925381 desktop-bold'}).text.strip()
            except:
                owner_name = soup.find('li', attrs={'data-label': 'additional-office-link',
                                                    'class': 'jsx-725757796 office-name'}).text.strip()
            try:
                mountly_cost = soup.find('td', attrs={'id': 'price_sqft-0', 'class': 'price_sqft'}).text.strip()

            except:
                try:
                    mountly_cost = soup.find('button', attrs={'class': 'jsx-2449308512 btn btn-link estimate-payment-link'}).find('span').text.strip()
                except:
                    mountly_cost = soup.find('div', attrs={'class':'jsx-488154125 ellipsis text-right'}).find('span', attrs={'class':'jsx-488154125 value ellipsis'}).text.strip()
            try:
                contact = soup.find('span', attrs={'data-label': 'additional-office-phone',
                                                   'class': 'jsx-725757796 visible-sm-inline visible-md-inline visible-lg-inline'}).text.strip()
            except:
                contact = 'No Contact'

            #  convert javascript
            converted_script = ''
            scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
            for script in scripts:
                if script:
                    converted_script = converted_script + script.contents[0]
            converted_script = re.sub(r"[@]", '', converted_script)

            # load file
            datas = json.loads(converted_script)
            with open('temp/results_detail.json', 'w+') as files:
                data_json = {
                    'results': datas
                }

                # writing json
                json.dump(data_json, files)

            print('Data Writed')

            # read json file
            with open('temp/results_detail.json', 'r') as json_file:
                result_data = json.load(json_file)
                print(f'Json Length: {len(result_data)}')

                # getting data
                address = [result['address']['streetAddress'] for result in result_data['results'] if
                           'address' in result]
                try:
                    postcode = \
                    [result['address']['postalCode'] for result in result_data['results'] if 'address' in result][0]
                except:
                    postcode = [result['address']['postalCode'] for result in result_data['results'] if
                                'address' in result]

                try:
                    footage = [result['floorSize'] for result in result_data['results'] if 'floorSize' in result][0]
                except:
                    footage = [result['floorSize'] for result in result_data['results'] if 'floorSize' in result]
                    if footage == []:
                        footage = "No Floor Size Data"
                try:
                    region = \
                    [result['address']['addressRegion'] for result in result_data['results'] if 'address' in result][0]
                except:
                    region = [result['address']['addressRegion'] for result in result_data['results'] if
                              'address' in result]
                try:
                    room = [result['numberOfRooms'] for result in result_data['results'] if 'numberOfRooms' in result][
                        0]

                except:
                    try:
                        room = soup.find('li', attrs={'class': 'jsx-2414508836'}).text.strip()
                    except:
                        room = [result['numberOfRooms'] for result in result_data['results'] if
                                'numberOfRooms' in result]

                # store item to dict
                data_dict = {
                    'street address': address,
                    'region': region,
                    'postcode': postcode,
                    'owner name': owner_name,
                    'contact': contact,
                    'square footage': footage,
                    'number_room': room,
                    'montly cost': mountly_cost,
                    'price': price
                }

                # append all item
                self.final_data.append(data_dict)

            # close the driver
            if self.use_selenium:
                driver.close()

            # create json for final data
            with open('realtor_temporary/final_data.json', 'w+') as final_json:
                json.dump(self.final_data, final_json)
                print(f"generate result from URL: {data['url']} ")

    def run(self):
        url = 'https://realtor.com/realestateandhomes-search/New-York_NY'
        res = self.get_response(url=url)
        if self.use_selenium:
            self.get_all_url(res)

        else:
            self.get_all_url(res.text)

        self.get_detail(self.results)


if __name__ == '__main__':
    scraper = RealtorScraper()
    scraper.run()

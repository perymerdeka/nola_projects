import requests
import json
import math
import os
from bs4 import BeautifulSoup
from selenium import webdriver


class ZillowScraper:
    results = []  # <- create list to append the result
    final_data_result = []  # <- Sore Final Data Result
    # headers
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
        'cache-control': 'max-age=0',
        # 'cookie':'zguid=23|%2482971312-d59b-4dbf-95e6-be130386df47; zgsession=1|5a99c9d4-4d68-4926-8ad9-645ef59232d3; _ga=GA1.2.1911770309.1609684744; _gid=GA1.2.567505807.1609684744; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; zjs_user_id=null; zjs_anonymous_id=%2282971312-d59b-4dbf-95e6-be130386df47%22; _gcl_au=1.1.432493643.1609684746; KruxPixel=true; DoubleClickSession=true; _pxvid=6e6f9ed3-4dd1-11eb-a0fb-0242ac12000e; _pin_unauth=dWlkPVpHUXlNR1JoTkRNdFpqUmlNUzAwT1dSa0xXSXpOMll0TjJJd05ESXdOV1ptTkRFdw; KruxAddition=true; g_state={"i_p":1609694581605,"i_l":1}; JSESSIONID=58F1189F61A4E62830C9E1577A776160; _px3=f7c3f9a333c148cb851665258ec4b7589cdc6db6b40183560c794a50097773ab:YQWzRQ3YL9ybVCojGYRFeEVm2CuOUepLnLgS8rxRLlb2JLJEy9DR7m5oVclE8ZWuwgIitoxFTAtaA3tMyA6/8A==:1000:WkYVEE+mCK+jlGnca7AJU9f49kQHr/dQx8h0ATyLNpFRW5k622JQK56sbVDbmQmgNXUcDlfWuH7ZjBvBSraH1T4Tc6WWXMNp9z+nhxODOlH7qAPF/d2O545/PxzCrWnON9y4eBftj0wc6whJLlxJgFqcG6vvcUDcbdaJ7i0YNCo=; _uetsid=6ee457b04dd111eba15027b6e0f16ac3; _uetvid=6ee4a5704dd111eb81fb1b375ee4179a; ki_r=; _gat=1; search=6|1612344715732%7Crect%3D41.2150938491687%252C-73.1429955625%252C40.1927894141644%252C-74.8129174375%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%096181%09%09%09%09%09%09; ki_s=; AWSALB=lHPoabWbXYbNGvKvYt1gxXP4nbu1VVgjApd8xBy4QV69bNnQFyo1zIS9OcZP3OGY3Yj//v+Lo0L9gaEm7Mc78Ebd7Ocb/00Z0l2Er7+nAk8ryv9gdjLhArC4SC1g; AWSALBCORS=lHPoabWbXYbNGvKvYt1gxXP4nbu1VVgjApd8xBy4QV69bNnQFyo1zIS9OcZP3OGY3Yj//v+Lo0L9gaEm7Mc78Ebd7Ocb/00Z0l2Er7+nAk8ryv9gdjLhArC4SC1g; ki_t=1609752622273%3B1609752622273%3B1609752727193%3B1%3B7',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    # fetch requests
    def get_response(self, url, params):
        """Directory Handling"""
        try:
            print('Creating Directory to Store Temp Item')
            os.makedirs('temporary_zillow')
        except FileExistsError:
            pass

        # requests Handle
        res = requests.get(url, params=params, headers=self.headers)
        f = open('temporary_zillow/res.html', 'w+')
        f.write(res.text)
        f.close()
        print(f'Response Status Code: {res.status_code}')
        return res

    def get_total_pages(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        pages = soup.find('span', attrs={'class': 'result-count'}).text.replace(',', '').split('result')[0]
        total_pages = math.ceil(int(pages) / 40)
        print('Total Page Founds: ', total_pages)
        return total_pages

    # scraping proccess to getting content
    def get_url(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        # scraping process
        container = soup.find('ul', attrs={'class': 'photo-cards photo-cards_wow photo-cards_short'})
        for card in container.contents:
            script = card.find('script', attrs={'type': 'application/ld+json'})
            if script:
                script_parser = script.contents[0]
                data_json = json.loads(script_parser)

                self.results.append(
                    {
                        'street Address': data_json['address']['streetAddress'],
                        'address region': data_json['address']['addressRegion'],
                        'address locality': data_json['address']['addressLocality'],
                        'postal Code': data_json['address']['postalCode'],
                        'url': data_json['url'],
                        'square footage': data_json['floorSize']['value'],
                        'price': card.find('div', attrs={'class': 'list-card-price'}).text.strip()

                    }
                )

        print('URL Per Page Found {}'.format(len(self.results)))
        return self.results

    def get_detail(self, filename_result, content_result):
        # driver path selenimum
        PATH = os.path.abspath(os.path.join(os.curdir, 'driver/chromedriver'))
        driver = webdriver.Chrome(PATH)
        # get json file
        with open('temporary_zillow/results.json', 'w+') as file:
            # generate result
            data_result = {
                'data_result': content_result,
            }
            json.dump(data_result, file)

        # dev mode
        content_result = content_result[0:2]

        # data person
        person = []
        for data in content_result:
            print('processing URL: {}'.format(data['url']))
            driver.get(data['url'])

            # content checking
            print('Getting Source... of URL: {}'.format(data['url']))
            f = open('temporary_zillow/res_detail.html', 'w+')
            f.write(driver.page_source)
            f.close()

            # getting Detail Content
            print('Parsing Content...')

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            container = soup.find('div', attrs={'class': 'ds-body-small'})
            contents = container.find_all('span', attrs={'class': 'hdp__sc-1al31ja-0 kRZUWS'})
            for info in contents:
                person.append(info.get_text())

            # get another info
            more_info = soup.find('ul', attrs={'class': 'sc-puFaA ePiitE'})
            items = more_info.find_all('span', attrs={'class': 'Text-c11n-8-18-0__aiai24-0 foiYRz'})
            mountly_cost = soup.find('h5', attrs={
                'class': 'Text-c11n-8-18-0__aiai24-0 StyledHeading-c11n-8-18-0__ktujwe-0 LJxVR sc-qQmou bViFbQ'}).text.strip()
            for item in items:
                person.append(item.get_text())

            # data dict
            data_dict = {
                'street address': data['street Address'],
                'address region': data['address region'],
                'state': data['address locality'],
                'postal Code': data['postal Code'],
                'montly cost': mountly_cost,
                'square footage': data['square footage'],
                'owner_name': person[0],
                'owner_contact': person[2],
                'bedroom': person[4],
                'bathroom': person[5],
            }

            # append final result to list
            self.final_data_result.append(data_dict)

        # creating directory to stored content
        try:
            print('Creating Directory')
            os.makedirs('zillow_result')

        except FileExistsError:
            print('directory Exists, Storing Result Content..')
            pass

        print('Total Scrapped URL', len(self.final_data_result))

        filename_result = filename_result.replace("//", "").replace("/", "_").replace(",", "").replace('rb_', 'rb').replace('https:', '')
        print('Generate Json File For {}'.format(filename_result))
        with open('zillow_result/{}.json'.format(filename_result), 'w+') as json_file:
            json.dump(self.final_data_result, json_file)

        print('{}.json Generated'.format(filename_result))

        driver.close()
        return self.final_data_result

    # create run func to run scraper
    def run(self):
        # params
        params = {
            'searchQueryState': '{"pagination":{},"usersSearchTerm":"New York, NY","mapBounds":{"west":-74.8129174375,"east":-73.1429955625,"south":40.42945465007956,"north":40.98120890098652},"regionSelection":[{"regionId":6181,"regionType":6}],"isMapVisible":true,"filterState":{"sortSelection":{"value":"globalrelevanceex"},"isAllHomes":{"value":true}},"isListVisible":true,"mapZoom":9}',
            'wants': '{"cat1":["listResults","mapResults"]}',
            'requestId': '4'
        }

        # define url
        url = 'https://www.zillow.com/homes/New-York,-NY_rb/'

        # getting response
        res = self.get_response(url, params=params)

        self.get_total_pages(res.text)
        self.get_url(res.text)

        # get result
        self.get_detail(content_result=self.results, filename_result=url)


if __name__ == '__main__':
    zillow_scraper = ZillowScraper()
    zillow_scraper.run()

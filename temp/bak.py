property_list = container.find_all('li', attrs={'data-testid': 'result-card'})
        street_address = container.find_all('div', attrs={'data-label':'pc-address'})
        for item in street_address:
            street = item.get_text()
            self.address.append(street)

        for prop in property_list:
            link = self.base_url + prop.find('a')['href']
            self.results.append(link)


# function helper to check captcha
    def check_captcha(self, html_response_file, url):
        session = HTMLSession()

        file = open(html_response_file, 'r')
        soup = BeautifulSoup(file, 'html.parser')

        # find title
        title = soup.title.string
        if title == "Pardon Our Interruption":
            print('Captcha Detected')
            res = session.get(url, headers=self.headers)
            res.html.render()
            return res

            # parsing content



 with open('json_results.json', 'w') as files:
                files.write(converted_script)
                files.close()

            print('json writed')

            # extract data from json file
            with open('json_results.json', 'r') as json_file:
                datas = json.load(json_file)
                print('checking Type: {}'.format(type(datas)))










# bot bypass
        bypass_params = 'Pardon Our Interruption'
        with open('realtor_temporary/res.html', 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
            title = soup.find('title').text.strip()
            if title == bypass_params:
                try:
                    print('Requests Blocked, Using Proxy...')
                    # proxies
                    auth = HTTPProxyAuth(username="aumgqnti-dest", password="df1erwe2bzvk")
                    response = requests.get(url, headers=self.headers, proxies={'https': 'https://' + self.get_proxy()}, timeout=3, auth=auth)
                    print(f'Proxy Use {response.json()}')
                    return response
                except:
                    try:
                        print('SSL ERROR try to auth proxy using different module...')
                        auth = HTTPProxyDigestAuth(username="aumgqnti-dest", password="df1erwe2bzvk")
                        respose_session = self.session.get(url, headers = self.headers, proxies={'https': 'https://' + self.get_proxy()}, auth=auth)
                        return respose_session

                    except:
                        print('SSL Error')
                        raise

f
title == bypass_params:
try:
    print('Using Proxy...')
    auth = HTTPProxyDigestAuth(username="aumgqnti-dest", password="df1erwe2bzvk")

    respose_session = self.session.get(url, headers=self.headers,
                                       proxies={'http': 'http://' + self.get_proxy()}, auth=auth)
    print(f'Using Proxy.. Site Status Code {respose_session.status_code}')

    print(f'Proxy Use {"http://" + self.get_proxy()}')
    return respose_session

except:
    print('SSL Error')
    raise
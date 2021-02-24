from random import choice
import json
import requests
from lxml.html import fromstring
import keyboard


class Socks_proxies:

    def __init__(self):
        self.proxy = None
        self.proxies = []

    @staticmethod
    def get_proxies():
        url = 'https://www.socks-proxy.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        p = []
        for i in parser.xpath('//tbody/tr'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            p.append(proxy)
        return p

    @staticmethod
    def to_proxy(proxy):
        return {"http": 'socks4://'+str(proxy), "https": 'socks4://'+str(proxy)}

    def get(self):
        if len(self.proxies) < 2:
            self.proxies = self.get_proxies()
        self.proxy = choice(self.proxies)
        return self.to_proxy(self.proxy)

    def remove(self):
        # Remove invalid proxy from pool
        self.proxies.remove(self.proxy)
        self.proxy = self.get()

    def scrape(self, url, **kwargs):
        # Retry until request was sucessful
        while keyboard.is_pressed('ctrl+q') == False:
            try:
                proxy = self.get()
                print("Proxy currently being used: {}".format(proxy))
                response = requests.get(url, proxies=proxy, timeout=2, **kwargs)

                f = open('socks4.txt','a')
                f.write('\n' + str(proxy['https']))
                f.close

                break
            # if the request is successful, no exception is raised
            except requests.exceptions.ProxyError:
                print("Proxy error, choosing a new proxy")
                self.remove()
            except requests.exceptions.ConnectTimeout:
                print("Connect error, choosing a new proxy")
                self.remove()
        return response
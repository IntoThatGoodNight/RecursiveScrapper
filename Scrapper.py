import re
from urlparse import  urljoin, urlsplit, SplitResult
import requests
from bs4 import BeautifulSoup
import sys

class RecursiveScraper:
    def __init__(self, url):
        self.domain = urlsplit(url).netloc
        self.mainurl = url
        self.urls = set()

    def preprocess_url(self, referrer, url):
        if not url:
            return None

        fields = urlsplit(urljoin(referrer, url))._asdict()
        fields['path'] = re.sub(r'/$', '', fields['path']) 
        fields['fragment'] = '' 
        fields = SplitResult(**fields)
        if fields.netloc == self.domain:
            if fields.scheme == 'http':
                httpurl = cleanurl = fields.geturl()
                httpsurl = httpurl.replace('http:', 'https:', 1)
            else:
                httpsurl = cleanurl = fields.geturl()
                httpurl = cleanurl = fields.geturl()
                httpurl = httpurl.replace('https:', 'http:', 1)
            if httpurl not in self.urls and httpsurl not in self.urls:
                return cleanurl

        return None

    def scrape(self, url=None):
       
        if url is None:
            url = self.mainurl

        print("Scraping {:s} ...".format(url))
        self.urls.add(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        for link in soup.findAll("a"):
            childurl = self.preprocess_url(url, link.get("href"))
            if childurl:
                self.scrape(childurl)


sys.setrecursionlimit(10000)
rscraper = RecursiveScraper("")
rscraper.scrape()
allUrls=[]
allUrls = rscraper.urls
print(rscraper.urls)
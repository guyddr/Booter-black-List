from lxml import html

from Crawler.crawler_api.booter_url import BooterURL
from Crawler.crawler_api.crawler import Crawler


# documentation: https://developers.google.com/web-search/docs/#The_Basics

class Crawler_Google2(Crawler):
    'Crawler of Google via default web requests'

    def __init__(this, sleep_level=1):
        domain = 'https://www.google.com/search?ie=UTF-8&num=100'
        Crawler.__init__(this, domain, sleep_level)
        this.PrintNote('CRAWLING GOOGLE2')
        this.PrintDivider()
        this.Initialize()

    # this.Header['referer'] = 'utwente.nl'

    # def Login(this):
    # no login
    # this.PrintError('NO LOGIN REQUIRED')

    # overrides Crawler's crawl function
    def Crawl(this, max_results=100):
        keywords = ['Booter', 'DDOSer', 'Stresser']

        nr_pages = int(max_results / 100)
        this.PrintUpdate('initiating crawling procedures: Google')

        for keyword in keywords:
            this.PrintDivider()
            this.PrintNote('KEYWORD: ' + keyword)
            this.PrintDivider()
            for i in range(0, nr_pages):
                counter = 0
                # dynamically generate search query
                query = "&q=" + keyword + '&start=' + str(i * 100) + '&filter=0'
                url = this.Target + query

                this.PrintDebug('crawling: ' + query)
                # read html and parse JSON
                response = this.JSCrawl(url)
                tree = html.fromstring(response.text)

                urls = tree.xpath('//*/div[@class="r"]/a/@href')

                split = 10
                for url in urls:
                    try:
                        # parse url
                        if '/url?q=' in url:
                            url = url[7:].split('&sa')[0]
                        this.AddToList(BooterURL(url), 'Google')

                        if counter % split == 0:
                            this.PrintDivider()
                        counter = counter + 1
                    except Exception as ex:
                        this.PrintError('EXCEPTION: ' + str(ex))
                this.Sleep()

        this.PrintUpdate('DONE; found ' + str(len(this.URLs)) + ' potential Booters')
        this.PrintDivider()

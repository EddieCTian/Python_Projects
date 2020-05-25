#basic web crawller
#pass in website through sysarg, no need for http://www.
#code trys the https version, then the http version. 
#recursive crawling

import requests
import re
from urllib.parse import urlparse
import sys

class  PyCrawler(object):
    def __init__(self, starting_url):
        secure='https://www.'+str(starting_url)
        regular='http://www.'+str(starting_url)
        try:
            requests.get(regular)
            self.starting_url=regular
        except:
            self.starting_url=secure
        self.visited=set()
        print(f"First Link: {self.starting_url}")

    def get_html(self,url):
        try:
            html=requests.get(url)
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('latin-1')
    
    def get_links(self, url):
        html=self.get_html(url)
        parsed=urlparse(url)
        base=f"{parsed.scheme}://{parsed.netloc}"
        links=re.findall('''<a\\s+(?:[^>]*?\\s+)?href="([^"]*)"''',html)
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base=base + link
                links[i]=link_with_base
        
        return set(filter(lambda x: 'mailto' not in x, links))

    def extract_info(self, url):
        html=self.get_html(url)
        meta=re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>",html)
        return dict(meta)
    
    def crawl(self, url):
        for link in self.get_links(url):
            if link in self.visited:
                continue
            print (link)
            self.visited.add(link)
            info=self.extract_info(link)

            print(f"""Link: {link}
            Description: {info.get('description')}
            Keywords: {info.get('keywords')}
            """)

            self.crawl(link)

    def start(self):
        self.crawl(self.starting_url)


#if __name__ == "__main__":
crawler=PyCrawler(sys.argv[1])
crawler.start()
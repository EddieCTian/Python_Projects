#sysarg 1 is starting url
#sysarg 2 is file name

import requests
import re
from urllib.parse import urlparse, urljoin
import sys
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import image_crawler


class  PyCrawler(object):
    def __init__(self, starting_url, folder):
        self.starting_url=starting_url
        self.visited=set()
        self.f=open(folder, "w")
        self.netlocation=urlparse(self.starting_url).netloc
        self.f.write(f"First Link: {self.starting_url}\n\n")
        self.cnt=0

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
        self.cnt +=1
        for link in self.get_links(url):
            if link in self.visited:
                continue
            if urlparse(link).netloc!=self.netlocation:
                continue
            self.visited.add(link)
            info=self.extract_info(link)

            self.f.write(
            '\n\n\nLink:'+link+
            '\nDescription:'+str(info.get('description'))+
            '\nKeywords:'+str(info.get('keywords'))+'\n'+
            'Image URLs:\n')
            
            #old code for putting website info into terminal, now writes to a file. 

            image_crawler.other_main(link, self.cnt, self.f)
            self.crawl(link)

    def start(self):
        self.crawl(self.starting_url)
        self.f.close()


#if __name__ == "__main__":
crawler=PyCrawler(sys.argv[1], sys.argv[2])
crawler.start()

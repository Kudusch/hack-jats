from dataclasses import dataclass
from time import struct_time
from author import Author
from bs4 import BeautifulSoup
import requests

@dataclass
class Article:
    title:str
    abstract:str
    published_date:struct_time
    authors:list[Author]
    doi:str
    volume:str
    number:str
    id:str
    link:str
    article_html:str

    @staticmethod
    def _parse_abstract(abst_xml):
        parsed = BeautifulSoup(abst_xml, parser='html.parser')
        chunks = list(parsed.strings)
        return chunks[-1]

    @staticmethod
    def _parse_authors(authors):
        return [Author.from_rssxml(author) for author in authors]

    @staticmethod
    def from_rssxml(entry):
        return Article(title = entry.get('title', ''),
                       abstract = Article._parse_abstract(entry.get('summary','')),
                       published_date = entry.get('published_parsed',None),
                       authors = Article._parse_authors(entry.get('authors','')),
                       doi = entry.get('prism_doi',''),
                       id = entry.get('id',''),
                       link = entry.get('link',''),
                       volume = entry.get('prism_volume',''),
                       number = entry.get('prism_volume',''))

    def get_pdf(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,de;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "SaneID=DKX0DdzPkbe-cbK0AYL; _ga=GA1.2.626144651.1615302341; OUP_SessionId=e2iiqyuayrfmkzqyrn51ytg5; Oxford_AcademicMachineID=637890703085116346",
            "Host": "academic.oup.com",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
            "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='101', 'Google Chrome';v='101'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "macOS"
        }


        result = requests.get(self.link, headers=headers)
        if result.ok == True: 
            self.article_html = result.content

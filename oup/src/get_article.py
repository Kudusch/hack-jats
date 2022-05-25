import feedparser
from article import Article

rss_feed = feedparser.parse(open("../OpenAccess.xml",'rb'))
articles = [Article.from_rssxml(entry) for entry in rss_feed['entries']]


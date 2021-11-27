from bs4 import BeautifulSoup
import requests



#Function mmorpg_scrape ,scrapes mmorpg.org.pl site and takes all latest news and get newest one
def mmorpg_scrape():
    r = requests.get('https://mmorpg.org.pl/')
    soup = BeautifulSoup(r.text,'html.parser')
    whole_article_div = soup.find("div",{"class" : "article-list"})
    articles = whole_article_div.find_all("div",{"class":"article-list__item"})

    news ={}
    for article in articles:
        name = article.find("h3",{"class":"article-list__item--title"})
        text = name.find("a").getText()
        url_short = name.find('a',href=True)
        url =f"https://mmorpg.org.pl{url_short['href']}"
        news[text]=url

    newest_news = list(news.items())[0]
    name = newest_news[0]
    url = newest_news[1]
    return name,url

name,url = mmorpg_scrape()

def mmorpg_post_image(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if (r.url).startswith('https://forum'):
        return None
    else:

        whole_article_div = soup.find("div",{"class":"content__left"})
        if whole_article_div is None:
            return
        article = whole_article_div.find("div",{"class":"article__text"})

        img = article.find("figure",{"class":"image-full"})
        img_url ="https://mmorpg.org.pl"+img.find("img")['src']
        return img_url



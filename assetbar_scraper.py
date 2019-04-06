from bs4 import BeautifulSoup
import requests as r
from time import sleep

prefix = "http://web.archive.org/web/20101024022544/http://m.assetbar.com:80/achewood/"

def parse_page(href):
    page = r.get(href).text
    soup = BeautifulSoup(page, "lxml")
    pageid = soup.select('span.prevnext a')[-1]['href']

    title = soup.select('#content > h2')[0].contents[0]
    date = soup.select('#content > h2 > span.date')[0].string

    print(pageid, title, date)
    return str(soup.select('#comments_pane')[0])

def __main__():
    try:
        with open("assetbar/cache.txt") as f:
            pageid = f.read().split("\n")[-1]
    except FileNotFoundError:
        pageid = "uua8XVqnr"
        
    while True:
        with open("assetbar/" + pageid + "_comments.html", 'w') as f:
            f.write(parse_page(prefix + pageid))

        with open("assetbar/cache.txt", "a") as f:
            f.write("\n" + pageid)
        
        sleep(3)

if __name__ == '__main__':
    __main__()

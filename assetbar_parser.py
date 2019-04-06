#!/bin/env python

from bs4 import BeautifulSoup
from sys import argv
from re import search
from json import dump

class Comment:
    def __init__(self, name, text, depth, snip, plus, minus):
        self.name = name
        self.text = text
        self.depth = depth
        self.snip = snip
        self.plus = plus
        self.minus = minus

    def __repr__(self):
       return "<Comment(depth='{depth}',name='{name}',text='{text}',snip='{snip}',plus='{plus}',minus='{minus}')>".format(**self.__dict__)

def parse_comment(comment):
    children = list(comment.children)
    spacer, guts = children[:2]
    depth = int(spacer['width']) // 30

    name = guts.select("span.name")
    text = guts.select("div.text")
    footer = guts.select("div.footer")
    if name and text:
        name = ' '.join(str(x) for x in name[0].contents).strip()
        text = ' '.join(str(x) for x in text[0].contents).strip()
        rating = ' '.join(str(x) for x in footer[0].select("span")[0].contents).strip()
        match = search('Comment rated (.*) Chubbies and (.*) Lames', rating)
        plus, minus = int(match.group(1)), int(match.group(2))
        snip = False
    else:
        guts = children[2]
        footer = guts.select("div.footer")
        text = footer[0].text.strip()
        text = ' '.join(text.split())
        plus = minus = 0
        name = search('left by ([^ ]*)', text).group(1)
        snip = True

    return Comment(name, text, depth, snip, plus, minus)


def parse_file(filename):
    soup = BeautifulSoup(open(filename).read(), 'lxml')

    tables = soup.select("tbody > tr > td > table > tr")
    comments = [parse_comment(table).__dict__ for table in tables]
    
    page_id = search("uu[A-Za-z0-9]*", filename).group(0)

    with open("json/{0}.json".format(page_id), "w") as f:
        dump(comments, f, indent=2, sort_keys=True)

if __name__ == '__main__':
    parse_file(argv[1])

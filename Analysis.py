#!/usr/bin/python

import mechanize
from BeautifulSoup import BeautifulSoup
def scrapeLinks(baseUrl,data):
    soup = BeautifulSoup(data)
    links = [mechanize.Link(baseUrl = baseUrl,
        url = str(anchor['href']),
        text = str(anchor.string),
        tag = str(anchor.name),
        attrs = [(str(name), str(value))
            for name,value in anchor.attrs])
        for anchor in soup.body.findAll('a',target="_blank",rel="nofollow")]
 
    return links

def main():
    baseUrl = "http://bj.meituan.com/"
    br = mechanize.Browser()
    data = br.open(baseUrl).get_data()
    links = scrapeLinks(baseUrl, data)

if __name__ == "__main__":
    main()
    print links

import re
import sys
import urllib.request
import urllib.parse

from urllib.parse import urlparse
from html.parser import HTMLParser

class Parser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    if ('http' not in value and 'https' not in value and 'page' in value):
                        self.pages.append(value[value.rfind('=') + 1:])

    def read_content(self, url):
        try:
            with urllib.request.urlopen(url) as response:
                if 'text/html' in response.getheader('Content-Type'):
                    bHtml = response.read()
                    html = bHtml.decode("utf-8")

                    return html
                else:
                    return ''
        except:
            print ('Not connected!')

    def find_last_page(self, url):
        self.last_page = 0
        self.pages = []
        self.baseUrl = url

        content = self.read_content(url)

        if content:
            self.feed(content)
            self.last_page = int(max(self.pages))
            return self.last_page, self.pages
        else:
            return 0, []

    def find_by_regex(self, regex, html):
        try:
            p = re.findall(r'{}'.format(regex), html);
            return p
        except:
            print ('Regex error!')
            return []

def craw(url_list, regex_list, output):  
    parser = Parser()

    urls = ''
    regex = ''

    with open(url_list,'r') as f:
        urls = f.readlines()

    with open(regex_list, 'r') as f:
        regex = f.readlines()

    if urls and regex: 
        for url in urls:
            url = url.rstrip().lstrip()

            last_page, pages = parser.find_last_page(url)
               
            if last_page > 0:
                print("Total page: ", last_page)

            page = 0

            while page != last_page:
                page = page + 1
                thread_url = url + '&page=' + str(page)

                print ("Crawling: ", thread_url)

                for r in regex:
                    r = r.rstrip().lstrip()
                    links = parser.find_by_regex(r, parser.read_content(thread_url))
                    if (links):
                        with open(output, 'a') as f:
                            for link in links:
                                f.write('{} {}'.format(link[1], '\n'))

if __name__ == "__main__":
    if len(sys.argv) > 3:
        craw(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print ('Usage: python crawler.py url_input_file regex_input_file output_file')
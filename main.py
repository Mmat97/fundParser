import sys
import requests
from bs4 import BeautifulSoup
import urllib.request 
import re
import lxml.etree as et
import io

FORMS_TO_SEARCH_FOR=['13F']

TEXT_TO_SEARCH_FOR_13F=['INFORMATION TABLE', '.xml']

PRE_LINK='https://www.sec.gov/'

def get_url(tickorcik):
    url='https://www.sec.gov/cgi-bin/browse-edgar?CIK='+ tickorcik + '&owner=exclude&action=getcompany'
    response=requests.get(url)
    c=response.content
    soup=BeautifulSoup(c,'html.parser')
    if("No matching" in soup.get_text()):
        print("Error: ticker does not match anything in database")
        print()
        return None
    #if get url filled with the information for a given ticker/cik, return it 
    return url


    #search/filter page of url for all documents matching 13-FHR
def handle_13FHR(url, forms):
    with urllib.request.urlopen(url) as response:
        page = response.read()
        soup = BeautifulSoup(page, 'html.parser')

        for tr in soup.find_all('tr'):
            td2 = tr.find_all('td')
            for td in td2:                
                if forms[0] in td.get_text():
                    for href in tr.find_all('a'):
                        if href.get('href').startswith('/Archive'):
                            document = href.get('href')
                            break#only want first document   
                    return document          








#the format of the 13F reports will differ Ex: same with infromation table as type and xml as document 
def check_13F_format(file_page):
        for tr in file_page.find_all('tr'):
            if(TEXT_TO_SEARCH_FOR_13F[0] in tr.get_text() and TEXT_TO_SEARCH_FOR_13F[1] in tr.get_text()):
                for a in tr.find_all('a', href=True):
                    return PRE_LINK+a['href']
                    


def get_holdings_table(archive_url):
    # download holdings documents page
    with urllib.request.urlopen(archive_url) as response:
        archive = response.read()
    soup = BeautifulSoup(archive, 'html.parser')
    return check_13F_format(soup)


    

def convert_holdings_tsv(fund_url):
    # download table
    with urllib.request.urlopen(fund_url) as response:
        table = response.read()

    # parse 
    soup = BeautifulSoup(table, 'lxml')

    re_table = re.compile('informationtable', re.I)
    soup.find(re_table).attrs = {}

    namespace = re.compile('^.+\:.+$', re.I)
    tag_title = re.compile('^.+\:(.+)$', re.I)

    for tag in soup.find_all(namespace):
        tag.name = tag_title.match(tag.name).group(1)

    soup = soup.find('informationtable')

    with open("13F_format.xsl", 'r') as xsl_file:
        xslt = et.parse(xsl_file)

    parsed = et.parse(io.StringIO(soup.prettify()))
    xsl_form = et.XSLT(xslt)
    output = xsl_form(parsed)

    return output



def main():
    if(len(sys.argv)==2):
        tickorcik=sys.argv[1]
        url=get_url(tickorcik)
        if(url==None):
            sys.exit()
        archive_link=PRE_LINK+handle_13FHR(url,FORMS_TO_SEARCH_FOR)
        holdings_table=get_holdings_table(archive_link)
        
        tsv_data = convert_holdings_tsv(holdings_table)
        with open('output.tsv', 'w') as tsvfile:
            tsvfile.write(str(tsv_data))
    else:
        print("Input ticker or CIK")
        sys.exit()



if __name__=='__main__':
    main()
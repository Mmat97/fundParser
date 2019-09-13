import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

FORMS_TO_SEARCH_FOR=['13F-HR']

def get_url(tickorcik):
    url='https://www.sec.gov/cgi-bin/browse-edgar?CIK='+ tickorcik + '&owner =exclude&action =getcompany'
    response=requests.get(url)
    c=response.content
    soup=BeautifulSoup(c,'html.parser')
    if("No matching" in soup.get_text()):
        print("Error: ticker does not match anything in database")
        print()
        return None
    #if get url filled with the information for a given ticker/cik, return it 
    return url


    #search/filter page of url using forms specified
def handle_13FHR():




def main():
    if(len(sys.argv)==2):
        tickorcik=sys.argv[1]
        url=get_url(tickorcik)
        if(url==None):
            sys.exit()
        
    else:
        print("Input ticker or CIK")
        sys.exit()



if __name__=='__main__':
    main()
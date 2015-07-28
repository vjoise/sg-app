#Get the Malls here

from bs4 import BeautifulSoup
import urllib2

MALL_SITE="http://comesingapore.com/tourist-directory/category/mall"
MALL_SITE_INDEX="http://comesingapore.com/tourist-directory/category/mall/~/#i"
output_file=open("C:/Deepthi/sg-app/malls.csv", 'w+')
def get_mall_url(url) :
    sp = BeautifulSoup(urllib2.urlopen(url).read())
    a_array=sp.find_all("a")
    for a1 in a_array :
        #print a1
        if a1.has_attr('onclick') and str(a1['href']).find('bookmark') == -1:
            print a1
            output_file.write(a1['href'] + ',' + 'Not started' + '\n')
    
def main(url) :
    req = urllib2.urlopen(url)
    soup = BeautifulSoup(req.read())
    all_a=soup.find_all("a")
    for a in all_a:
        if a.has_attr('id') and str(a['href']).find('review') >=0:
            get_mall_url("http://comesingapore.com"+a['href']);

#call this for the first page.
main(MALL_SITE)

#call this for the remaining set of pages.
for index in range(1, 8):
    url=str(MALL_SITE_INDEX).replace('#i', str(index*10));
    main(url)

output_file.close();

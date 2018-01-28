import urllib2 as u
from bs4 import BeautifulSoup as bs


def extracttags(url):

    hdr = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    req = u.Request(url, headers=hdr)
    doc = u.urlopen(req).read()
    soap =  bs(doc, 'html.parser')
    lst = soap.select('.a-unordered-list.a-nostyle.a-button-list.a-declarative.a-button-toggle-group.a-horizontal.a-spacing-top-micro.swatches.swatchesSquare')

    print "Tags"

    for item in lst:
        try:
            tags = item.select('.a-size-base')
            for tag in tags:
				print tag.string
           
        except:
            pass

    print '\n'

def search(term):
    url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords='+term
    hdr = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    req = u.Request(url, headers=hdr)
    doc = u.urlopen(req).read()
    soap =  bs(doc, 'html.parser')
    lst = soap.select('.s-result-item.celwidget')
    #with open('data/'+term+'.query','w') as f:
    for item in lst:
        try:
            image_url = item.select_one('.s-access-image.cfMarker')['src']
            product = item.select_one('.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal')
            product_text = product['title']
            product_link = product['href']
            seller = item.select_one('.a-size-small.a-color-secondary').next_sibling.string
            price = item.select_one('.sx-price-whole').string
            rating = item.select_one('.a-icon.a-icon-star .a-icon-alt').string
            print '\n'.join([product_text,image_url , product_link, seller, price,rating,'\n'])
            extracttags(product_link)

            # print(product_text+'\n')
        except:
            pass

        
search('pencil')
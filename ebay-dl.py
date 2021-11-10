import argparse
import requests
from bs4 import BeautifulSoup
import json

def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string.

    >>> parse_itemssold('48 sold')
    48
    >>> parse_itemssold('24 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

def parse_itemprice(text):
    '''
    Takes input with $ or range and returns the price of the item in cents.

    >>> parse_itemprice('$20.50')
    2050
    >>> parse_itemprice('$69.99 to $99.99')
    6999
    >>> parse_itemprice('$201.99')
    20199
    >>> parse_itemprice('$2,199.99')
    219999
    '''
    x = 0
    y = 0
    p = ''
    price = 0
    for i in range(len(text)):
        text = text.replace(',','')
        x = text.find('$')
        y = text.find('.')
        p = text[x+1:y]
        p += text[y:y+3]
        [num, dec] = p.rsplit('.')
        price += int(num.replace('.', ''))*100
        price += int(dec)
        return price
    else:
        return None
        
def parse_itemshipping(text):
    '''
    Takes as input a string and returns the shipping cost, as specified in the string.

    >>> parse_itemshipping('+$10.50 shipping')
    1050
    >>> parse_itemshipping('+$8.09 shipping')
    809
    >>> parse_itemshipping('Free shipping')
    0
    ''' 
    x = 0
    y = 0
    s = ''
    shipping = 0
    for i in range(len(text)):
        if text == 'Free shipping':
            return 0
        else:
            x = text.find('$')
            y = text.find('.')
            s = text[x+1:y]
            s += text[y:y+3]
            [num, dec] = s.rsplit('.')
            shipping += int(num.replace('.', ''))*100
            shipping += int(dec)
            return shipping


# this if statement says only run the code below when the python file is run normally (not in the doctests)

if __name__ == '__main__':

    # get command line arguments
    parser = argparse.ArgumentParser(description='Donwload info from eBay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    args = parser.parse_args()
    print("args.search_term=", args.search_term)

    items = []

    # loop over the ebay webpages
    for page_number in range(1,int(args.num_pages)+1):
        
        # build the url
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + args.search_term + '&_sacat=0&_pgn=' + str(page_number)
        print('url=',url)
        

        # download the html
        r = requests.get(url)
        status=r.status_code
        print('status=',status)
        html=r.text
        # print('html=',html[:50])
        
        # process the html
        soup = BeautifulSoup(html, 'html.parser')

        # loop over the items in the page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items:
            print('tag_item=', tag_item)

            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                name = tag.text
            
            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_itemprice(tag.text)

            status = None
            tags_status = tag_item.select('.s-item__subtitle')
            for tag in tags_status:
                status = tag.text

            shipping = None
            tags_shipping = tag_item.select('.s-item__shipping')
            for tag in tags_shipping:
                shipping = parse_itemshipping(tag.text)

            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns=True

            items_sold = None
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)

            
            item = {
                'name': name,
                'price': price,
                'status': status,
                'shipping': shipping,
                'free_returns': freereturns,
                'items_sold': items_sold,
            }
            items.append(item)

        print('len(tag_items)=', len(tags_items))

        for item in items:
            print('item=', item)

    print('len(items)=', len(items))

    # write the json to a file
    filename = args.search_term+'.json'
    with open (filename, 'w', encoding='ascii') as f:
        f.write(json.dumps(items))
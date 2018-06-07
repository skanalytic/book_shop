from bs4 import BeautifulSoup
import requests
import pandas as pd


output_dir = '../data/isbn_tracker_data.csv'

## NEED TO CONNECT THIS WITH ISBN RDF SCANNER / KEYBOARD INPUT
isbn_list = ['9781908276407','9781908276506','9781564784360','9780811223430','9780292719620']

dfout = pd.DataFrame({'isbn':[],'isbn_status':[],'url':[],'title':[],'author':[],'publisher':[],'bookformat':[],'language':[]})
for isbn in isbn_list:
    ## NEED TO ADD MORE ROBUST CHECKS
    isbn = str(isbn).replace('-','')

    if len(isbn) == 13:
        generic_url = 'https://www.bookfinder.com/search/?author=&title=&lang=en&isbn={}&new_used=*&destination=de&currency=EUR&mode=basic&st=sr&ac=qr'
        full_url = generic_url.format(isbn)
        isbn_good = 'OK'
    elif len(isbn) == 10:
        generic_url = 'https://www.bookfinder.com/search/?author=&title=&lang=en&isbn=+{}+&new_used=*&destination=de&currency=EUR&mode=basic&st=sr&ac=qr'
        full_url = generic_url.format(isbn)
        isbn_good = 'OK'
    else:
        print("not isbn format")
        isbn_good = 'BAD'
        author = ''
        publisher = ''
        bookformat = ''
        language = ''

    ## NEED TO FIGURE OUT WHY SO SLOW (COULD SWITCH TO SCRAPY ETC.)
    resp = requests.get(full_url)
    r = requests.get(full_url)
    data = r.text
    soup = BeautifulSoup(data,"lxml")

    title = soup.find(id="describe-isbn-title").text
    author = soup.find(itemprop="author").get_text()
    publisher = soup.find(itemprop="publisher").get_text()
    bookformat = soup.find(itemprop="bookformat").get_text()
    language = soup.find(itemprop="inLanguage").get_text()

    print(title,author,publisher,bookformat,language)
    dftemp = pd.DataFrame({'isbn':[isbn],'isbn_status':[isbn_good],'url':[full_url],'title':[title],'author':[author],'publisher':[publisher],'bookformat':[bookformat],'language':[language]})
    dfout = dfout.append(dftemp)


## NEED TO CONNECT THIS TO A PROPER (SERVER) DB E.G. POSTGRES SQL (& SIMPLE FRONT-END APP)
dfout.to_csv(output_dir,index=False)

## MAY ALSO WANT SOME SERVER LOGIC TO DEDUPE / ADD CALCULATION FIELDS ETC.
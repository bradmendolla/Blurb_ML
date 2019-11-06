from bs4 import BeautifulSoup
from splinter import Browser

# set params
def blurb_scrape(url):
    i = 0
    executable_path = {'executable_path': '/home/brad/Documents/Novel-blurb-NLP/chromedriver'}
    browser = Browser('chrome', **executable_path)
    for i in range(0, 200, 2):
        #open browser and navigate list
        
        try:
            browser.visit(url)
        
            link = browser.find_link_by_partial_href('/book/show/')[i]
            link.click()
            #need this for some reason otherwise it prints
            html = browser.html
            blurb_soup = BeautifulSoup(html, 'html.parser')
        
            try:
                div = blurb_soup.find('div', class_ = 'readable stacked')
                title = blurb_soup.find('h1').text
            
                blurb = div.find_all('span')[1].text
                print(title)
                print(blurb)
                print("----------------------------------------------------------")
            

            except IndexError:
                div = blurb_soup.find('div', class_ = 'readable stacked')
                title = blurb_soup.find('h1').text
                blurb = div.find_all('span')[0].text
                print(title)
                print(blurb)
                print('----------------------------------------------------------')
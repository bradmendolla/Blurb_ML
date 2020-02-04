from bs4 import BeautifulSoup
from splinter import Browser
import pymongo



conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.Blurbs



def blurb_scrape(url):
    i = 0
    executable_path = {'executable_path': '/home/brad/Documents/Novel-blurb-NLP/chromedriver'}
    browser = Browser('chrome', **executable_path, headless = True)
    for i in range(0, 200, 2):
        browser.visit(url)
        link = browser.links.find_by_partial_href('/book/show/')[i]
        link.click()
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', class_ = 'readable stacked')
        try:
            title = soup.find('h1').text
            author = soup.find('div', class_ = 'authorName__container').text
            blurb = div.find_all('span')
            if len(blurb) == 2:
                post = {
                    "title" : title,
                    "author" : author,
                    'blurb' : blurb[1].text
            }
                collection.insert_one(post)
                browser.back()
            elif len(blurb) == 1:
                post = {
                    "title" : title,
                    "author" : author,
                    'blurb' : blurb[0].text
            }
                collection.insert_one(post)
                browser.back()
            else:
                browser.back()
        except (AttributeError, IndexError):
            browser.back()
            continue

def loop_scrape(url):
    print("Loop Start")
    blurb_scrape(url)
    executable_path = {'executable_path': '/home/brad/Documents/Novel-blurb-NLP/chromedriver'}
    browser = Browser('chrome', **executable_path, headless = True)
    browser.visit(url)
    browser.is_element_present_by_text('Next', wait_time = 3)
    next_elem = browser.links.find_by_partial_text('Next').first
    next_elem.click()
    new_url = browser.url
    browser.quit()
    count = 0
    while (count < 100):
        count += 1
        print(f"Page {count} scraped.")
        try:
            blurb_scrape(new_url)
            executable_path = {'executable_path': '/home/brad/Documents/Novel-blurb-NLP/chromedriver'}
            browser = Browser('chrome', **executable_path, headless = True)
            browser.visit(new_url)
        
            browser.is_element_present_by_text('Next', wait_time = 3)
            next_elem = browser.links.find_by_partial_text('Next').first
            next_elem.click()
            new_url = browser.url
            browser.quit()
        except:
            break

  


collection = db.romance


loop_scrape('https://www.goodreads.com/list/show/12362.All_Time_Favorite_Romance_Novels?page=10')
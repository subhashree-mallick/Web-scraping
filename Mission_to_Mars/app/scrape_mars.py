#import Splinter, beautifulsoup,and browser
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def init_browser():
    executable_path={"executable_path":"c:\\Users\\subha\\.wdm\\drivers\\chromedriver\\win32\\89.0.4389.23\\chromedriver.exe"}
    return Browser("chrome",**executable_path,headless=True)

def scrape_all():
    browser=init_browser()
    news_title,news_p=mars_news()
    featured_image_url=featured_image()
    #facts =mars_facts()
    #hemisphere=hemispheres()
    mars_data={
        'news_title':news_title,
        'news_p':news_p,
        'featured_image_url':featured_image_url,
        'facts':mars_facts(),
        'hemispheres':hemispheres(),
        'last_modified':dt.datetime.now()
    } 
     # Stop webdriver and return data
    browser.quit()
    return mars_data

def mars_news():
    browser=init_browser()
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Add try/except for error handling
    
    try:
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        slide_elem = soup.select_one('ul.item_list li.slide')
        news_title = slide_elem.find("div", class_='content_title').get_text()
        news_p = soup.find("div", class_="article_teaser_body").get_text()
        
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image():
    browser=init_browser()
    # Visit URL
    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(image_url)
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return featured_image_url


def mars_facts():
    url='https://space-facts.com/mars/'
    # Add try/except for error handling
    try:
        df=pd.read_html(url)[0]
        
    except BaseException:
        return None

    # assign columns and set index of dataframe
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format
    mars_table= df.to_html()
    return mars_table


def hemispheres():
    browser=init_browser()
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Click the link, find the sample anchor, return the href
    hemisphere_image_urls = []
    for i in range(4):
        # Find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
        hemi_data = scrape_hemisphere(browser)
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemi_data)
        # Finally, we navigate backwards
        browser.back()

    return hemisphere_image_urls


def scrape_hemisphere(browser):
    #browser=init_browser()
    # parse html text
    html_text = browser.html
    hemi_soup = BeautifulSoup(html_text, 'html.parser')

    # adding try/except for error handling
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")
        
    except AttributeError:
        # Image error will return None, for better front-end handling
        title_elem = None
        sample_elem = None

    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemispheres
   

if __name__ == "__main__":
    #print(mars_news())
    print(scrape_all())
    #print(hemispheres())
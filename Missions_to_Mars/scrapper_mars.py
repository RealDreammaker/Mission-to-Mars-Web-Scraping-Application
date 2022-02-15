# import dependancies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
    
def scrape():
    # initialize chrome browser using splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    
    ##### NASA Mars News
    ###### Scrape the Mars News Site and collect the latest News Title and Paragraph Text
    # visit browser
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # ensure sufficient time for browser to load
    time.sleep(1)

    # parse the website to html
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # getting the latest new, should always be the first on the list
    lastest_title =  soup.find("div", class_= "content_title").text
    lastest_news =  soup.find("div", class_= "article_teaser_body").text
  


    ##### JPL Mars Space Images - Featured Image
    # visit browser
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # ensure sufficient time for browser to load
    time.sleep(1)

    # parse the website to html
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    image_rel_path = soup.find("img", class_= "headerimage fade-in")["src"] 
    # complete image path
    featured_image_url = url + image_rel_path
    


    ##### Mars Facts
    # visit browser
    url = "https://galaxyfacts-mars.com/"

    # parse html to dataframe table
    table = pd.read_html(url)

    # keeping the comparable data 
    df1 = table[0]

    # set first row column names 
    df1.columns = df1.iloc[0]
    df1 = df1.iloc[1:]
    
    # convert comparable data to html
    html_mars_earth = df1.to_html(classes="table table-striped table-hover", justify= "left", col_space = "33%", border = 1, index = False)
    html_mars_earth

    # keeping the comparable data 
    df2 = table[1]
    
    # convert comparable data to html
    html_mars_fact = df2.to_html(classes="table table-dark table-hover ", header = False, justify= "left", col_space = "33%", border = 1, index = False)
    html_mars_fact



    ##### Mars Hemispheres
    # visit browser
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # ensure sufficient time for browser to load
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html,"html.parser")

    # getting text links to the hemispheres by looping through h3
    hemisphere_titles = []
    for item in soup.find_all("h3"):
        # except for h3 with text content of "Back", store titles to variables
        if item.text != "Back":
            hemisphere_titles.append(item.text.strip())

    hemisphere_titles

    # navigate to the link found above
    hemisphere_image_urls = []
    for title in hemisphere_titles:
        browser.links.find_by_partial_text(title).click()
        
        # parse the website to html
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        items = soup.find_all("li")
        for item in items:
            try:
                if item.a.text == "Sample":
                    img_link = url + item.a["href"]
                    hemisphere_image_urls.append({
                        "title": title,
                        "img_url": img_link
                    })
                    break 
            except AttributeError:                       
                pass
        # return to the previous page
        browser.links.find_by_partial_text("Back").click()

    hemisphere_image_urls

    # store data in a dictionary variable
    scraped_data = {
        "news_title": lastest_title,
        "news_p":lastest_news,
        "featured_image_url": featured_image_url,
        "mars_earth": html_mars_earth,
        "mars_fact": html_mars_fact,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # exit browser
    browser.quit()

    return scraped_data

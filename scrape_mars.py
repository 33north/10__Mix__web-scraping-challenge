# Scraping script

# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as rq
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import time
import pprint as pp

# executable_path = {"executable_path": ChromeDriverManager().install()}
# chrome = Browser("chrome", **executable_path, headless = True)

time_variable = 1

def mars_website_scrape(browser):
    # Mars website
    mars_url = "https://redplanetscience.com/"
    browser.visit(mars_url)

    # Let the website load otherwise it might not be able to grab html
    time.sleep(time_variable)

    html_mars = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    mars_soup = bs(html_mars, "html.parser")

    # Get title of news article
    news_title = mars_soup.select_one("div.list_text").find("div", class_ = "content_title").get_text()

    # Get news short article
    news_article = mars_soup.select_one("div.list_text").find("div", class_ = "article_teaser_body").get_text()

    return news_title, news_article

def nasa_website_scrape(browser):
    # Nasa website
    nasa_url = "https://spaceimages-mars.com/"
    browser.visit(nasa_url)

    # Let the website load otherwise it might not be able to grab html
    time.sleep(time_variable)

    html_nasa = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    nasa_soup = bs(html_nasa, "html.parser")

    # Get the image url for the header image on nasa
    featured_image_url = nasa_soup.find("img", class_ = "headerimage").get("src")
    featured_image_url = nasa_url + featured_image_url

    return featured_image_url

def mars_fact_website_scrape():
    # Mars fact website 
    mars_fact_url = pd.read_html("https://galaxyfacts-mars.com/")[1]
    mars_fact_url = mars_fact_url.rename(columns = {0: "Mars Planet Profile", 1: "Facts"})

    # Convert mars data to html
    mars_fact_html = mars_fact_url.to_html()

    return mars_fact_html

def mars_hemi_website_scrape(browser):
     # Mars hemishere website
    mars_hemi_url = "https://marshemispheres.com/"
    browser.visit(mars_hemi_url)

    # Let the website load otherwise it might not be able to grab html
    time.sleep(time_variable)

    html_mars_hemi = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    mars_hemi_soup = bs(html_mars_hemi, "html.parser")

    hemisphere_image_urls = []

    # Grab all div tags in first webpage
    mars_hemi_soup_divtag = mars_hemi_soup.find_all("div", class_ = "description")

    # for-loop through div tag in mars_hemi_soup_divtag
    for div_tag_first in mars_hemi_soup_divtag:
        hemi_title = div_tag_first.find("h3").get_text()
        hemi_image_link = div_tag_first.find("a").get("href")
        next_page_img_link = mars_hemi_url + hemi_image_link

        # Visit the subsequent page for the hemisphere image
        browser.visit(next_page_img_link)
        html_mars_hemi_next = browser.html

        # Create BeautifulSoup object; parse with 'html.parser'
        mars_hemi_soup_next = bs(html_mars_hemi_next, "html.parser")

        # Grabb all div tags of the subsequent page
        mars_hemi_soup_next_divtag = mars_hemi_soup_next.find_all("div", class_ = "downloads")

        # for-loop through div tag in mars_hemi_soup_next_divtag
        for div_tag_second in mars_hemi_soup_next_divtag:
            hemi_full_link = div_tag_second.find("a").get("href")
            full_mars_hemi_url = mars_hemi_url+hemi_full_link

            hemi_dict = {
                "title": hemi_title,
                "img_url": full_mars_hemi_url
            }
            
            # Append title and full image link into list
            hemisphere_image_urls.append(hemi_dict)

    return hemisphere_image_urls

# def scrape_mars_info(browser):
#     # executable_path = {"executable_path": ChromeDriverManager().install()}
#     # browser = Browser("chrome", **executable_path, headless = True)

#     news_title, news_article = mars_website_scrape(browser)
#     featured_image_url = nasa_website_scrape(browser)
#     mars_fact_html = mars_fact_website_scrape()
#     hemisphere_image_urls = mars_hemi_website_scrape(browser)
#     scrape_dict = {
#         "mars_news_title": news_title,
#         "mars_bews_article": news_article,
#         "nasa_featured_image": featured_image_url,
#         "mars_facts": mars_fact_html,
#         "mars_hemispheres": hemisphere_image_urls
#     }

#     # Turn this on to see content of dictionary
#     # pp.pprint(scrape_dict)

#     return scrape_dict

def scrape_mars_info():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless = True)

    news_title, news_article = mars_website_scrape(browser)
    featured_image_url = nasa_website_scrape(browser)
    mars_fact_html = mars_fact_website_scrape()
    hemisphere_image_urls = mars_hemi_website_scrape(browser)
    scrape_dict = {
        "mars_news_title": news_title,
        "mars_news_article": news_article,
        "nasa_featured_image": featured_image_url,
        "mars_facts": mars_fact_html,
        "mars_hemispheres": hemisphere_image_urls
    }

    # Turn this on to see content of dictionary
    # pp.pprint(scrape_dict)

    return scrape_dict

# scrape_mars_info(chrome)

if __name__ == "__main__":
    # pp.pprint(scrape_mars_info(browser))
    pp.pprint(scrape_mars_info())
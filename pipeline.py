import sys
import logging

import threading
from collectData import *
from selenium import webdriver

def usage(status):
    print ("Usage: ./collectData [keyword] [n] [t]")
    print ("")
    print ("     - keyword needs to be in quotations")
    print ("     - n is the top n links in search result (< 5)")
    print ("     - t is the time out in minutes")

    sys.exit(status)


def get_links(keyword, number,driver_path):
  
    # Set url
    keyword = keyword.replace(' ', '+')
    url = "https://www.youtube.com/"
    url = url + "results?search_query=" + keyword # search query
    url = url + "&sp=EgJAAVAU" # live stream filter

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')

   # driver = webdriver.Chrome(driver_path+"/chromedriver",chrome_options=options)
    driver = webdriver.Chrome(chrome_options=options)    
    driver.get(url)

    videos = driver.find_elements_by_tag_name('ytd-video-renderer')

    # Store links in list
    links = []
    n = 0
    for video in videos:
        thumb = video.find_element_by_id('thumbnail')
        link = thumb.get_attribute('href').encode('utf-8')
        links.append(link)

        n = n + 1
        if n == number:
            break

    driver.close()

    return links


def pipeline_run(links):
    driver_path = os.getcwd()
    # Parse command line argument
    #if len(sys.argv) != 4:
    #    usage(1)

    #keyword = sys.argv[1]
    #number = int(sys.argv[2])
    #timeout = int(sys.argv[3])
    #keyword = kw
    number = 2
    timeout = 10
    #if number < 1 or number > 4:
    #    usage(1)

    #links = list()
    #links = get_links(keyword,number,driver_path)

    # Set flag and lock for shutdown
    shutdown = False
    threads = []

    # Start threads to crawl data
    for link in links:
        print("Starting thread for link: " + link.decode('utf-8'))
        t = threading.Thread(target = crawl_link, args=(link.decode('utf-8'), lambda: shutdown,))
        threads.append(t)
        t.start()

    # This blocks specified timeout
    print("Beginning countdown...")
    time.sleep(timeout*60)

    # Change flag to signal threads to shutdown
    shutdown = True
    print("Preparing to shutdown...")

    for t in threads:
        t.join()

    sys.exit(0)

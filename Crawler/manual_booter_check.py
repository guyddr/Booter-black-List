import datetime
import sys

from selenium import webdriver

import Crawler.crawler_api.storage
from Crawler.crawler_api.booter_url import BooterURL


# this is a simple script to manually traverse all PBDs found by the crawler
# this script uses Selenium to open each PBD and quickly stores data based on
# a keypress; used for generating training/test datasets.
# this is a convenience script as manually retyping and saving URL data takes
# a considerate amount of time.

def getch():
    import tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


from_date = datetime.datetime(2015, 8, 10).strftime('%Y-%m-%d %H:%M:%S')  # date of specific test items

# open chrome driver
driver = webdriver.Chrome()

# get all domains to check
for url in Crawler.crawler_api.storage.Select('SELECT fullURL FROM urls WHERE timeAdd >= \'' + str(from_date) + '\''):
    function_key_pressed = False

    while not function_key_pressed:
        booterURL = BooterURL(url[0])
        driver.get(booterURL.Full_URL)

        ch = getch()
        if ch == 'n':
            print('N PRESSED')
            Crawler.Crawler.crawler_api.storage.Update('urls', booterURL.UniqueName(), '[booter?]', 'N')
            Crawler.crawler_api.storage.Update('urls', booterURL.UniqueName(), 'notes', 'manual')
            function_key_pressed = True
        elif ch == 'y':
            print('Y PRESSED')
            Crawler.crawler_api.storage.Update('urls', booterURL.UniqueName(), '[booter?]', 'Y')
            Crawler.crawler_api.storage.Update('urls', booterURL.UniqueName(), 'notes', 'manual')
            function_key_pressed = True
        elif ch == 'q':
            print('Q PRESSED')
            Crawler.crawler_api.storage.Update('urls', booterURL.UniqueName(), '[booter?]', '?')
            Crawler.crawler_api.storage.Update('urls', booterURL.UniqueName(), 'notes', 'manual')
            function_key_pressed = True
        elif ch == 'o':
            print('O PRESSED')
            Crawler.crawler_api.storage.Update('urls', booterURL.UniqueName(), '[booter?]', '?')
            Crawler.crawler_api.storage.Update('urls', booterURL.UniqueName(), '[status]', 'off')
            Crawler.crawler_api.storage.Update('urls', booterURL.UniqueName(), 'notes', 'manual')
            function_key_pressed = True
        else:
            print('NO FUNCTION KEY PRESSED')

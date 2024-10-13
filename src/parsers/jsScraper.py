from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import threading

def spinning_cursor():
    while not done:
        for cursor in '|/-\\':
            sys.stdout.write(f'\rParsing is in progress... {cursor}')
            sys.stdout.flush()
            time.sleep(0.1)

driver = webdriver.Chrome()
url = "https://colorhunt.co/palettes/random"

# Start the spinner in a separate thread
done = False
spinner_thread = threading.Thread(target=spinning_cursor)
spinner_thread.start()

# start scrapping
driver.get(url)
max_scrolls = 10
scroll_count = 0

last_height = driver.execute_script("return document.body.scrollHeight")
while scroll_count < max_scrolls:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        # If the height hasn't changed, we've reached the end of the content
        break

    last_height = new_height
    scroll_count += 1

with open("colorhunt_palettes_rendered.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

# Stop the spinner
done = True
spinner_thread.join()

print("Rendered HTML content saved to colorhunt_palettes_rendered.html")

driver.quit()
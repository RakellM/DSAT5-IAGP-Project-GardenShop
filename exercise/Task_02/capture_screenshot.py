import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'index.html'))
file_url = f"file:///{html_path.replace(os.sep, '/')}"

output_img = os.path.abspath(os.path.join(os.path.dirname(__file__), 'dashboard_screenshot.png'))

print(f"Loading {file_url} ...")

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1600,1100")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)
try:
    driver.get(file_url)
    time.sleep(2)  # Wait for Chart.js rendering and table population
    driver.save_screenshot(output_img)
    print(f"Screenshot successfully saved to: {output_img}")
finally:
    driver.quit()

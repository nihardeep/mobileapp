from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

try:
    driver = webdriver.Chrome(options=options)
    driver.get('file:///Users/nihardip/Desktop/Mobile design proptype/index.html')
    
    # Check for console errors on load
    logs = driver.get_log('browser')
    for log in logs:
        print(f"LOAD LOG: {log}")
        
    time.sleep(1)
    
    # Try to click Passenger 2
    try:
        el = driver.find_element("id", "passenger-card-2")
        el.click()
        print("Successfully clicked passenger-card-2")
    except Exception as e:
        print(f"Failed to click: {e}")
        
    # Check console again
    logs = driver.get_log('browser')
    for log in logs:
        print(f"POST-CLICK LOG: {log}")

    driver.quit()
except Exception as e:
    print(f"Selenium failed: {e}")

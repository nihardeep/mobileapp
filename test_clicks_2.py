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
    time.sleep(1)
    
    # 1. Switch to passenger screen
    driver.execute_script("document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));")
    driver.execute_script("document.getElementById('screenPassenger').classList.add('active');")
    time.sleep(1)
    
    # 2. Click passenger 2
    try:
        driver.execute_script("document.getElementById('passenger-card-2').click();")
        print("Successfully clicked passenger-card-2 via JS")
    except Exception as e:
        print(f"Failed to click via JS: {e}")
        
    time.sleep(1)
    
    # Check console
    logs = driver.get_log('browser')
    for log in logs:
        print(f"LOG: {log['level']} - {log['message']}")

    driver.quit()
except Exception as e:
    print(f"Selenium failed: {e}")

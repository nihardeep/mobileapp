from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
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
    driver.execute_script("document.getElementById('passenger-card-2').click();")
    time.sleep(1)
    
    # 3. Enter name and select wheelchair
    driver.execute_script("document.getElementById('pf-fname').value = 'Test Name';")
    driver.execute_script("document.getElementById('pf-assistance').value = 'Wheelchair';")
    
    # 4. Click save
    driver.execute_script("savePassengerForm();")
    time.sleep(1)
    
    # 5. Check if wheelchair text is on card 2
    card2_html = driver.execute_script("return document.getElementById('passenger-card-2').innerHTML;")
    if "Wheelchair Requested" in card2_html:
        print("SUCCESS: Wheelchair text is on the card.")
    else:
        print("FAIL: Wheelchair text is MISSING from the card.")
        print(card2_html)
        
    # Check console
    logs = driver.get_log('browser')
    for log in logs:
        print(f"LOG: {log['level']} - {log['message']}")

    driver.quit()
except Exception as e:
    print(f"Selenium failed: {e}")

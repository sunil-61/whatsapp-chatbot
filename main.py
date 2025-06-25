from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from reply_engine import get_reply

# WhatsApp Contact/Group
TARGET = "your-user-name" 


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--user-data-dir=./User_Data")  

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://web.whatsapp.com")
print("📲 Please scan the QR Code (if not already logged in)...")

try:
    wait = WebDriverWait(driver, 180)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Chat list"]')))
    print("✅ WhatsApp loaded!")

    
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Search input textbox"]')))
    search_box.click()
    sleep(1)
    search_box.send_keys(TARGET)
    sleep(2)

    chat = wait.until(EC.presence_of_element_located((By.XPATH, f'//span[@title="{TARGET}"]')))
    chat.click()
    print(f"📥 Opened chat with: {TARGET}")

    last_msg = ""

    while True:
        print("⏳ Checking for new messages...")
        messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]//span[contains(@class, "selectable-text")]/span')
        print(f"📨 Found {len(messages)} incoming messages.")

        if messages:
            msg = messages[-1].text.strip()
            print(f"📩 Last message: {msg}")
            if msg != last_msg:
                reply = get_reply(msg)
                print(f"🤖 Bot Replying: {reply}")

                # ✅ Correct input box
                input_box = driver.find_element(By.XPATH, '//footer//div[@contenteditable="true"]')
                input_box.send_keys(reply)
                input_box.send_keys("\n")

                last_msg = msg
        else:
            print("⚠️ No messages found.")
        sleep(2)

except Exception as e:
    print("❌ ERROR:", e)
    driver.quit()

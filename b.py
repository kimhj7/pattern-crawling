import time
import subprocess
import pyautogui
import pyperclip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
options.add_argument('--window-size=1920,1020')
#options.add_argument("disable-gpu")
options.add_argument("--no-sandbox")
options.add_experimental_option("detach", True)


# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options) # <- options로 변경
driver2 = webdriver.Chrome(service=service, options=options) # <- options로 변경

# 초기 페이지로 이동
driver.get("https://bloghelper.co.kr/k.php")
elem = driver.find_element(By.CLASS_NAME, 'roadGrid--bd5fc')
elem2 = elem.find_element(By.TAG_NAME, 'svg')
elem3 = elem2.find_element(By.TAG_NAME, 'svg')
elem4 = elem3.find_element(By.TAG_NAME, 'svg')
elem5 = elem4.find_element(By.TAG_NAME, 'svg')
elem6 = elem5.find_element(By.TAG_NAME, 'svg')
elem7 = elem6.find_elements(By.TAG_NAME, 'svg')

for e in elem7:
    try:
        text_to_input = e.get_attribute('name')
        if text_to_input is None:
            pass
        else:
            text_to_input = text_to_input[:6]
            if text_to_input == "Player":
                input = "P"
            else:
                input = "B"
            print(input)

    except IndexError:
        pass

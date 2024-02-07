import time
import subprocess
import pyautogui
import pyperclip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
options.add_argument('--window-size=1920,1020')
options.add_argument("--no-sandbox")
options.add_experimental_option("detach", True)


# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options) # <- options로 변경

# 초기 페이지로 이동
driver.get("https://www.lan5445.com")

last_window_handle = driver.current_window_handle

# 특정 파라미터가 포함된 URL을 찾은 후 업데이트를 중지하기 위한 플래그
update_completed = False

while True:
    # 업데이트가 완료된 경우 루프 중지
    if update_completed:
       break

    try:
        # 현재 열려 있는 모든 창의 핸들 가져오기
        window_handles = driver.window_handles

        # 새 창이 열렸는지 확인
        for window_handle in window_handles:
            if window_handle != last_window_handle:
                # 새로 열린 창으로 전환
                driver.switch_to.window(window_handle)

                # 새 창의 URL 확인
                current_url = driver.current_url

                # URL에 특정 파라미터가 포함되어 있는지 확인
                if "game=baccarat" in current_url:
                    print("특정 파라미터가 포함된 새 창 URL:", current_url)
                    time.sleep(3)
                    driver.switch_to.frame(driver.find_element(By.TAG_NAME,"iframe"))
                    time.sleep(3)
                    elem = driver.find_element(By.CLASS_NAME, 'roadGrid--bd5fc')
                    text_to_input = elem.get_attribute('outerHTML')
                    pyperclip.copy(text_to_input)
                    subprocess.Popen(['notepad.exe'])
                    time.sleep(2)  # 메모장이 실행될 때까지 잠시 대기
                    pyautogui.hotkey('ctrl', 'v')

                    update_completed = True


        # 리소스 사용 최소화를 위해 잠시 대기
        time.sleep(1)
    except KeyboardInterrupt:
        # 사용자가 Ctrl+C를 누르면 루프 종료
        break

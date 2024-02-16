import time
import subprocess
import pyautogui
import pyperclip

import tkinter as tk
from tkinter import *

win = Tk()
win.geometry('400x200')
win.title("더블X패턴")
win.attributes("-topmost", True)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from screeninfo import get_monitors

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
options.add_argument('--window-size=1920,1020')
#options.add_argument("disable-gpu")
options.add_argument("--no-sandbox")


monitors = get_monitors()
if monitors[0].width < 1367:
    options.add_argument("force-device-scale-factor=0.5");
    options.add_argument("high-dpi-support=0.5");
elif monitors[0].width > 1367 and monitors[0].width < 1610:
    options.add_argument("force-device-scale-factor=0.6");
    options.add_argument("high-dpi-support=0.6");
elif monitors[0].width > 1610 and monitors[0].width < 1900:
    options.add_argument("force-device-scale-factor=0.7");
    options.add_argument("high-dpi-support=0.7");
elif monitors[0].width > 1900 and monitors[0].width < 2500:
    options.add_argument("force-device-scale-factor=0.8");
    options.add_argument("high-dpi-support=0.8");
elif monitors[0].width > 2500 and monitors[0].width < 3000:
    options.add_argument("force-device-scale-factor=0.9");
    options.add_argument("high-dpi-support=0.9");
elif monitors[0].width > 3000:
    options.add_argument("force-device-scale-factor=1");
    options.add_argument("high-dpi-support=1");

options.add_experimental_option("detach", True)

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
#driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경
#driver2 = webdriver.Chrome(service=service, options=options)  # <- options로 변경


last_opened_window_handle = True


def set_chrome_window_size(driver, width, height, x_offset=0, y_offset=0):
    driver.set_window_position(x_offset, y_offset)
    driver.set_window_size(width, height)
def reset(driver, driver2):
    last_window_handle = driver.current_window_handle
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
                        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
                        time.sleep(3)
                        elem = driver.find_element(By.CLASS_NAME, 'roadGrid--bd5fc')
                        inputdoublex(elem, driver, driver2)
                        crawlresult(driver, driver2)

                        update_completed = True

            # 리소스 사용 최소화를 위해 잠시 대기
            time.sleep(1)
        except KeyboardInterrupt:
            # 사용자가 Ctrl+C를 누르면 루프 종료
            break

def crawlresult(driver, driver2):

    while True:
        if not last_opened_window_handle:
            break

        try:
            current_url = driver.current_url

            # URL 변경 감지
            if "game=baccarat&table_id" not in current_url:
                break

            element = driver.find_element(By.CSS_SELECTOR, '[class*="gameResult"]')
            # 엘리먼트의 HTML 내용 가져오기
            element_html = element.get_attribute('innerHTML').strip()

            # HTML 내용이 비어있지 않은지 확인
            if element_html:
                # 주어진 함수 실행
                number_player = driver.find_element(By.CSS_SELECTOR, '.player--d9544 .score--9b2dc')
                number_banker = driver.find_element(By.CSS_SELECTOR, '.banker--7e77b .score--9b2dc')
                player = number_player.get_attribute('innerText')
                banker = number_banker.get_attribute('innerText')
                p_input = driver2.find_element(By.CLASS_NAME, "player")
                b_input = driver2.find_element(By.CLASS_NAME, "banker")
                submit_button = driver2.find_element(By.CLASS_NAME, "submit")
                p_input.click()
                p_input.send_keys(player)
                b_input.click()
                b_input.send_keys(banker)
                submit_button.click()
                time.sleep(10)
            else:
                time.sleep(1)

        except NoSuchWindowException:
            print("마지막 창이 닫혔습니다. 새 창을 확인합니다.")
            reset(driver, driver2)
            break

        except KeyboardInterrupt:
            # 사용자가 Ctrl+C를 누르면 루프 종료
            break
        except Exception as e:
            print(f"오류 발생: {e}")
            break

def inputdoublex(arg2, driver, driver2):
    element = arg2
    elem2 = element.find_element(By.TAG_NAME, 'svg')
    elem3 = elem2.find_element(By.TAG_NAME, 'svg')
    elem4 = elem3.find_element(By.TAG_NAME, 'svg')
    elem5 = elem4.find_element(By.TAG_NAME, 'svg')
    elem6 = elem5.find_element(By.TAG_NAME, 'svg')
    elem7 = elem6.find_elements(By.TAG_NAME, 'svg')
    finish_check = driver.find_element(By.CLASS_NAME, 'svg--47a93')

    update_completed = False
    while True:
        if len(finish_check.find_elements(By.TAG_NAME, 'svg')) == 0:
            driver2.refresh()

        # 업데이트가 완료된 경우 루프 중지
        if update_completed:
            break

        try:
            # 현재 페이지의 제목 가져오기
            current_title = driver2.title

            # 이전 페이지 제목과 현재 페이지 제목이 다를 경우 출력
            if current_title == "더블X패턴":

                for e in elem7:
                    try:
                        text_to_input = e.get_attribute('name')

                        if text_to_input is None:
                            pass
                        else:
                            previous_title = ""
                            p_button = driver2.find_element(By.CSS_SELECTOR, ".pattern_group2 .ct-p")
                            b_button = driver2.find_element(By.CSS_SELECTOR, ".pattern_group2 .ct-b")
                            t_button = driver2.find_element(By.CSS_SELECTOR, ".pattern_group2 .ct-t")
                            if "Tie" in text_to_input:
                                text_to_input = text_to_input
                            else:
                                text_to_input = text_to_input[:6]
                            if text_to_input == "Player":
                                p_button.click()
                            elif text_to_input == "Banker":
                                b_button.click()
                            elif "Banker Tie" in text_to_input:
                                b_button.click()
                                t_button.click()
                            elif "Player Tie" in text_to_input:
                                p_button.click()
                                t_button.click()
                            elif text_to_input == "Banker TiePlayer":
                                b_button.click()
                                t_button.click()
                    except IndexError:
                        pass
                update_completed = True
            else:
                time.sleep(1)
        except KeyboardInterrupt:
            # 사용자가 Ctrl+C를 누르면 루프 종료
            break
        except Exception as e:
            print(f"오류 발생: {e}")
            break

def findurl(driver, driver2):
    last_opened_window_handle = None
    last_checked_url = ""
    global docrawl

    while True:
        current_window_handles = driver.window_handles

        if not current_window_handles:
            print("열린 창이 없습니다. 새 창을 기다립니다.")
            time.sleep(1)
            continue

        # 현재 열려 있는 창 중 마지막 창을 선택
        # 마지막에 열린 새 창이 항상 선택되도록 last_opened_window_handle 업데이트
        new_last_opened_window_handle = current_window_handles[-1]
        if new_last_opened_window_handle != last_opened_window_handle:
            last_opened_window_handle = new_last_opened_window_handle
            driver.switch_to.window(last_opened_window_handle)
            driver.set_window_size(width - 120, height)
            last_checked_url = ""  # URL 체크 리셋

        try:
            current_url = driver.current_url

            # URL 변경 감지
            if current_url != last_checked_url:
                print("URL 변경 감지:", current_url)
                last_checked_url = current_url

                if "game=baccarat&table_id" in current_url:
                    print("필요한 URL 변경을 감지했습니다. 작업을 수행합니다.")
                    driver2.refresh()
                    time.sleep(5)
                    iframes = driver.find_elements(By.TAG_NAME, "iframe")
                    # iframe이 하나 이상 있을 경우 첫 번째 iframe으로 이동
                    if len(iframes) > 0:
                        driver.switch_to.frame(iframes[0])
                    time.sleep(1)
                    elem = driver.find_element(By.CLASS_NAME, 'roadGrid--bd5fc')

                    inputdoublex(elem, driver, driver2)
                    crawlresult(driver, driver2)

            time.sleep(1)  # 리소스 최소화를 위해 대기

        except NoSuchWindowException:
            print("마지막 창이 닫혔습니다. 새 창을 확인합니다.")
            driver2.refresh()
            last_opened_window_handle = None  # 창 닫힘 감지 시 핸들 초기화
        except KeyboardInterrupt:
            print("사용자에 의해 중단됨")
            break
        except Exception as e:
            print(f"오류 발생: {e}")
            break

def doAction(arg, driver, driver2):

    # 초기 페이지로 이동
    driver.get(arg)
    driver2.get("http://pattern2024.com/bbs/login.php")

    findurl(driver, driver2)

def main(a):
    global width
    global height

    if monitors[0].width < 1367:
        width = monitors[0].width * 1.05
        height = monitors[0].height * 1.6
    elif monitors[0].width > 1367 and monitors[0].width < 1610:
        width = monitors[0].width / 1.1
        height = monitors[0].height * 1.5
    elif monitors[0].width > 1610 and monitors[0].width < 1900:
        width = monitors[0].width / 1.35
        height = monitors[0].height * 1.2
    elif monitors[0].width > 1900 and monitors[0].width < 2500:
        width = monitors[0].width / 1.65
        height = monitors[0].height * 1.1
    elif monitors[0].width > 2500 and monitors[0].width < 3000:
        width = monitors[0].width / 1.68
        height = monitors[0].height / 1.1
    elif monitors[0].width > 3000:
        width = monitors[0].width / 3
        height = monitors[0].height / 1.8
    driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경
    driver2 = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(width - 120, height)
    driver.set_window_position(0, 0)
    driver2.set_window_size(width - 120, height)
    driver2.set_window_position(width - 120, 0)

    doAction(a, driver, driver2)


label1 = Label(win, text = "접속할 게임사이트 URL")
label1.grid(row=0, column=0)
entry1 = Entry(win, width = 20, bg = "white")
entry1.grid(row=0, column=1)

button = Button(win, text="클릭", command = lambda: main(entry1.get()))
button.grid(row=0, column=2)

win.mainloop()
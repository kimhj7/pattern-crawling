import time
import subprocess
import tkinter.messagebox
import os
import sys

import pyautogui
import pyperclip
import requests
import uuid
import tkinter as tk
from tkinter import *
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame0")

win = Tk()
win.geometry('900x450')
win.configure(bg = "#3A7FF6")
win.title("더블X패턴")
win.attributes("-topmost", True)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, StaleElementReferenceException
from screeninfo import get_monitors

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
options.add_argument('--window-size=1920,1020')
# options.add_argument("disable-gpu")
options.add_argument("--no-sandbox")

monitors = get_monitors()
if monitors[0].width < 1367:
    options.add_argument("force-device-scale-factor=0.45")
    options.add_argument("high-dpi-support=0.45")
elif monitors[0].width > 1367 and monitors[0].width < 1610:
    options.add_argument("force-device-scale-factor=0.6")
    options.add_argument("high-dpi-support=0.6")
elif monitors[0].width > 1610 and monitors[0].width < 1900:
    options.add_argument("force-device-scale-factor=0.7")
    options.add_argument("high-dpi-support=0.7")
elif monitors[0].width > 1900 and monitors[0].width < 2500:
    options.add_argument("force-device-scale-factor=0.8")
    options.add_argument("high-dpi-support=0.8")
elif monitors[0].width > 2500 and monitors[0].width < 3000:
    options.add_argument("force-device-scale-factor=0.9")
    options.add_argument("high-dpi-support=0.9")
elif monitors[0].width > 3000:
    options.add_argument("force-device-scale-factor=1.3")
    options.add_argument("high-dpi-support=1.3")

options.add_experimental_option("detach", True)

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
# driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경
# driver2 = webdriver.Chrome(service=service, options=options)  # <- options로 변경


last_opened_window_handle = True

serial_number = "MASTER"


def get_external_ip():
    response = requests.get('https://httpbin.org/ip')
    ip = response.json()['origin']
    return ip


def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
    return mac


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
    click_listener_script = """
    document.querySelector('div.content--82383 > .commonUiElement > .bottom-right--235ec > .box--51c3f > div > .wrapper--bafc9:nth-child(3) > button').addEventListener('click', function(event) {      
        alert('이전 게임 창 반드시 종료 후 다른방 입장');
        return false;
    });
    """
    # root > div > div > div.content--82383 > div:nth-child(10) > div.bottom-right--235ec > div > div > div:nth-child(3) > button
    driver.execute_script(click_listener_script)
    while True:

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
                        e.is_displayed()
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

                    except StaleElementReferenceException:
                        print("요소가 사라졌습니다. 다른 작업을 수행합니다.1")
                        break

                    except IndexError:
                        pass
                    except Exception as ex:
                        print(f"오류 발생: {ex}")
                        break
                update_completed = True
            else:
                time.sleep(1)

        except StaleElementReferenceException:
            print("요소가 사라졌습니다. 다른 작업을 수행합니다.")
            break

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
                    driver2.refresh()
                    time.sleep(5)
                    iframes = driver.find_elements(By.TAG_NAME, "iframe")
                    # iframe이 하나 이상 있을 경우 첫 번째 iframe으로 이동
                    if len(iframes) > 0:
                        driver.switch_to.frame(iframes[0])

                    elem = driver.find_element(By.CLASS_NAME, 'roadGrid--bd5fc')
                    inputdoublex(elem, driver, driver2)
                    time.sleep(5)
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


def main(a, b):
    sp = b.split(",")
    if sp[0] == "1":
        tkinter.messagebox.showwarning("동시 사용오류", "다른곳에서 동시접속 사용중입니다.\n사용중인 아이피 : %s" % sp[1])
    else:
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
            width = monitors[0].width / 2.5
            height = monitors[0].height / 1.5
        driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경
        driver2 = webdriver.Chrome(service=service, options=options)
        driver.set_window_size(width - 120, height)
        driver.set_window_position(0, 0)
        driver2.set_window_size(width - 120, height)
        driver2.set_window_position(width - 120, 0)

        doAction(a, driver, driver2)


def on_closing():
    url = "http://15.165.159.63/close_program.php"
    datas = {
        'serial_number': serial_number,
        'mac': get_mac_address(),
        'ip': get_external_ip()
    }
    response = requests.post(url, data=datas)
    win.destroy()


url = "http://15.165.159.63/serial_check.php"
datas = {
    'serial_number': serial_number,
    'mac': get_mac_address(),
    'ip': get_external_ip()
}

response = requests.post(url, data=datas)
t = response.text

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def resource_path(relative_path):
    """ 리소스의 절대 경로를 얻기 위한 함수 """
    try:
        # PyInstaller가 생성한 임시 폴더에서 실행 중일 때의 경로
        base_path = sys._MEIPASS
    except Exception:
        # 일반적인 Python 인터프리터에서 실행 중일 때의 경로
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

canvas = Canvas(
    win,
    bg = "#3A7FF6",
    height = 450,
    width = 900,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    425.9999999999999,
    7.105427357601002e-15,
    899.9999999999999,
    450.0,
    fill="#FCFCFC",
    outline="")

logo_image = PhotoImage(
    file=resource_path(os.path.join("assets", "logo.png"))
)
canvas.create_image(180,130,image=logo_image)

canvas.create_text(
    458.9999999999999,
    80.0,
    anchor="nw",
    text="사이트URL 입력",
    fill="#505485",
    font=("Roboto Bold", 32 * -1)
)

canvas.create_rectangle(
    42.999999999999886,
    234.0,
    111.99999999999989,
    241.0,
    fill="#FCFCFC",
    outline="")

entry_image_1 = PhotoImage(
    file=resource_path(os.path.join("assets", "entry_1.png"))
)

entry_bg_1 = canvas.create_image(
    651.9999999999999,
    215.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#DDE2EE",
    fg="#000716",
    font=("Roboto Bold", 18 * -1),
    highlightthickness=0
)
entry_1.place(
    x=470.9999999999999,
    y=179.0,
    width=362.0,
    height=71.0
)

canvas.create_text(
    42.999999999999886,
    292.0,
    anchor="nw",
    text="DOUBLE X PATTERN 접속기",
    fill="#FCFCFC",
    font=("Roboto Bold", 25 * -1)
)

button_image_1 = PhotoImage(
    file=resource_path(os.path.join("assets", "button_1.png"))
)
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command = lambda: main(entry_1.get(), t),
    relief="flat"
)
button_1.place(
    x=507.9999999999999,
    y=309.0,
    width=270.0,
    height=82.5
)
button_1.bind("<Enter>", button_1.config(cursor="hand2"))
button_1.bind("<Leave>", button_1.config(cursor=""))
canvas.create_text(
    730,
    419.0,
    anchor="nw",
    text="SERIAL NO. %s" % serial_number,
    fill="#a0a0a0",
    font=("ZCOOLXiaoWei Regular", 14 * -1)
)

win.resizable(False, False)
win.protocol("WM_DELETE_WINDOW", on_closing)
win.mainloop()
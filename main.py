
import win32gui
import win32con
import subprocess
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("--no-sandbox")
options.add_experimental_option("detach", True)


# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options) # <- options로 변경

driver.get("https://www.google.com")

def print_chrome_titles():
    def enum_window_callback(hwnd, titles):
        # 창의 클래스 이름을 검사하여 'Chrome_WidgetWin_1'인 경우만 처리합니다.
        # 이는 크롬 브라우저 창의 클래스 이름입니다.
        # 참고: 크롬의 버전이나 설정에 따라 클래스 이름이 다를 수 있습니다.
        if 'Chrome_WidgetWin_1' in win32gui.GetClassName(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:  # 제목이 비어있지 않은 경우에만 추가
                titles.append(title)
    titles = []
    win32gui.EnumWindows(enum_window_callback, titles)
    for title in titles:
        print(title)

# 함수 실행
time.sleep(5)

current_url = driver.current_url

def find_chrome_window(title):
    def callback(hwnd, extra):
        if title in win32gui.GetWindowText(hwnd):
            extra.append(hwnd)
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

def send_message_to_chrome(title, message, wparam=0, lparam=0):
    windows = find_chrome_window(title)
    for hwnd in windows:
        win32gui.SendMessage(hwnd, message, wparam, lparam)
def print_chrome_window_title(url):
    def enum_window_callback(hwnd, regex):
        if 'Chrome_WidgetWin_1' in win32gui.GetClassName(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if url in title:  # 제목에 특정 URL이 포함되어 있는지 확인
                print(title)
    win32gui.EnumWindows(enum_window_callback, None)


# 예제: 'Google - Google Chrome'이 제목인 창을 찾아 최소화합니다.
chrome_title = driver.title
send_message_to_chrome(chrome_title, win32con.WM_SYSCOMMAND, win32con.SC_MINIMIZE)

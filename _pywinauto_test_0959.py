from playwright.sync_api import sync_playwright, Page
import win32gui
import win32process
from pywinauto import Application
import json
import os
import re

class BrowserAutomation:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(channel="chrome", headless=False)
        self.context = None
        self.page = None
        self.title = None

    def open_page(self, url):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto(url)
        self.title = self.page.title()
        print(f"Page Title: {self.title}")

    def pause(self):
        self.page.pause()

    def close_browser(self):
        if self.page:
            self.page.close()
        self.browser.close()
        self.playwright.stop()

    def get_application(self):
        app = Application(backend="win32").connect(title_re=f".*{self.tilte}.*Chrome.*")
        return app
    
    def get_chrome_hwnd_and_pid(self):
        hwnd_pid = []
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                titles = win32gui.GetWindowText(hwnd)
                if self.title in titles:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    hwnd_pid.append((hwnd, pid, titles))
        win32gui.EnumWindows(callback, None)
        return hwnd_pid
    
    def get_application(self):
        hwnd_pid = self.get_chrome_hwnd_and_pid()

        if hwnd_pid:
            pid = hwnd_pid[0][1]
            return Application(backend="uia").connect(process=pid)
        else:
            raise Exception("No Chrome window found")

class BiliBili:
    def __init__(self):
        self.URL = "https://bilibili.com"
        self.UID = "445510184@qq.com"
        # self.PWD = input("请输入密码：")
        reg_match = re.search(r'https:\/\/(.*)\.', self.URL).group(1)
        self.COOKIE_FILE = f"{reg_match}_cookies.json"
        self.LOGIN_SELECTOR = ".header-login-entry"
        self.AVATAR_SELECTOR = ".header-entry-avatar"

    def save_cookies(self, context):
        cookies = context.cookies()
        with open(self.COOKIE_FILE, "w", encoding="utf-8") as f:
            json.dump(cookies, f)
        print("Cookies saved.")

    def load_cookies(self, context):
        if not os.path.exists(self.COOKIE_FILE):
            return False
        with open(self.COOKIE_FILE, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        print("Cookies loaded.")
        return True
    
    def is_logged_in(self, page: Page):
        try:
            page.wait_for_selector(self.AVATAR_SELECTOR, timeout=10000, state="attached")
            print("Already logged in.")
            return True
        except:
            print("Not logged in.")
            return False

    def login_with_password(self, page: Page, context):
        print("Logging in with username and password...")
        page.locator(".header-login-entry").click()
        page.get_by_role("textbox", name="请输入账号").fill(self.UID)
        page.get_by_role("textbox", name="请输入密码").fill(input("请输入密码："))
        page.click(".btn_primary")
        if self.is_logged_in(page):
            page.wait_for_timeout(1000)
            self.save_cookies(context)
            print("Login successful.")
        else:
            print("Login failed.")

    def login_web(self, page: Page, context):
        if self.load_cookies(context):
            page.reload()
            if self.is_logged_in(page):
                print("Logged in with cookies.")
            else:
                print("Cookies expired")
                self.login_with_password(page, context)
        else:
            self.login_with_password(page, context)

def main():
    target = BiliBili()

    # Initialize the automation class
    bot = BrowserAutomation()

    # Open the page
    bot.open_page(target.URL)
    target.login_web(bot.page, bot.context)
    # Connect to the application
    app = bot.get_application()
    print(f"Connected to Application: {app}")

    dlg = app.top_window()
    dlg.set_focus()

    dlg.type_keys('^l')
    dlg.type_keys(f'{target.URL}{{ENTER}}', with_spaces=True)

    try:   
        with bot.page.expect_popup() as page1_info:
            bot.page.get_by_role("textbox").click()
            bot.page.get_by_role("textbox").fill("excel")
            dlg.type_keys('{ENTER}')
            bot.page.wait_for_timeout(1000)
            page1 = page1_info.value
            titles = page1.eval_on_selector_all(
                ".bili-video-card__info--tit",
                "elements => elements.map(e => e.textContent.trim())"
            )
            print("<<<<<<<<<<<<<<<<<<<<     视频标题     >>>>>>>>>>>>>>>>>>>>>")
            for t in titles:
                print(t)
    except Exception as e:
        print(f"Error: {e}")
    
    # Pause the script to keep the browser open
    bot.pause()
    bot.close_browser()

main()
import win32gui
import win32con
import win32api
import pyautogui
import time
from pynput import mouse
import threading

def click_at(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def find_hwnd(text):
    def callback(hwnd, extra):
        title = win32gui.GetWindowText(hwnd)
        if text in title and win32gui.IsWindowVisible(hwnd):
            extra.append(hwnd)
    found = []
    win32gui.EnumWindows(callback, found)
    return found[0] if found else None


hwnd = find_hwnd("Clash for Windows")
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(hwnd)

left, top, right, bottom = win32gui.GetWindowRect(hwnd)
print("窗口坐标：", left, top, right, bottom)

def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        rel_x = x - left
        rel_y = y - top
        print(f"\n【鼠标点击】绝对坐标: ({x}, {y}), 相对窗口坐标: ({rel_x}, {rel_y})")

listener = mouse.Listener(on_click=on_click)
listener.start()

def on_move():
    try:
        while True:
            x, y = pyautogui.position()
            rel_x = x - left
            rel_y = y - top
            print(f"鼠标绝对坐标: ({x}, {y})  相对窗口坐标: ({rel_x}, {rel_y})", end='\r')
            time.sleep(0.1)

        
    except KeyboardInterrupt:
        print("\n结束")
        listener.stop()

# on_move()
target_x = left + 100
target_y = top + 426
click_at(target_x, target_y)
target_x = left + 1226
target_y = top + 199
click_at(target_x, target_y)
target_x = left + 1106
target_y = top + 202
click_at(target_x, target_y)

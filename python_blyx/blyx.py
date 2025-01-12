#————————后台控制——————————
#1获取窗口句柄、窗口坐标、宽高
#2后台鼠标点击
#3后台控制人物移动
#4程序遮罩

import pygetwindow as gw
from win32 import win32api, win32gui
from win32.lib import win32con
import time

class Hero:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.hwnd = 0
        self.get_hwnd()

    #获取窗口句柄
    def get_hwnd(self):
        # window = gw.getWindowsWithTitle("百炼英雄")[0]
        # self.hwnd = window._hWnd
        try:
            window = gw.getWindowsWithTitle("百炼英雄")[0]
        
        except IndexError:
            print('没有找到 百炼英雄 窗口。。。')
            return False
        
        else:
            self.hwnd = window._hWnd
            window.restore()    #恢复窗口

            self.x = window.left
            self.y = window.top
            self.w = window.width
            self.h = window.height

            print(self.x, self.y, self.w, self.h)
        
    #鼠标点击
    def do_click(self, position_x, position_y, flag):
        self.get_hwnd()
        # 宏 
        long_position = win32api.MAKELONG(int(position_x), int(position_y))
        #鼠标左键按下
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN,0,long_position)
        # time.sleep(0.05)
        my_time_sleep(0.05,flag)
        #鼠标左键抬起
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP,0,long_position)

    #控制人物移动
    def move(self, dir, move_time, flag):
        if flag == True:
            self.get_hwnd()
            w = self.w
            h = self.h
            x0 = int(0.5*self.w)
            y0 = int(0.785*self.h)
            lp = win32api.MAKELONG(x0, y0)

            px, py = 0,0
            if dir == "w":
                px, py = x0, y0 - 30
            
            lp2 = win32api.MAKELONG(int(px),int(py))
            #鼠标按下lp位置
            self.do_click(0.5*w, 0.98*h,flag)
            my_time_sleep(0.05, flag)
            win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, lp)
            #鼠标移动到 lp2位置
            my_time_sleep(0.05, flag)
            win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, lp2)
            #鼠标保持时间
            my_time_sleep(move_time,flag)
            #鼠标抬起
            win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lp2)


    #屏蔽
    def disable_mouse_input(self):
        old_style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
        new_style = old_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, new_style)

    #解除屏蔽
    def enable_mouse_input(self):
        old_style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
        new_style = old_style & ~win32con.WS_EX_LAYERED & ~win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, new_style)

#时间函数
def my_time_sleep(sleep_time, flag):
    t = time.time()
    while flag:
        if time.time() - t > sleep_time:
            return 0


if __name__ == "__main__":
    p = Hero()
    # print(p.hwnd)
    # p.do_click(333/610*p.w,421/1113*p.h,1)
    p.disable_mouse_input()
    p.move("w",5,flag=1)
    p.enable_mouse_input()
    
    

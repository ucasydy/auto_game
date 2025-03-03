#————————后台控制——————————
#1获取窗口句柄、窗口坐标、宽高
#2后台鼠标点击
#3后台控制人物移动
#4程序遮罩

import pygetwindow as gw
from win32 import win32api, win32gui
from win32.lib import win32con
import time

import win32ui
from ctypes import windll
import numpy as np
import cv2


# 引入 Windows API 常量(截图使用)
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040

from ultralytics import YOLO
# Load a model
#card_best 训练的分类：
"""
"reboot_bt": 0,  # ...
"reboot": 1,    # 重启小程序
"fdj":2,        #放大镜
"T_BOX":3,      #宝箱
"RED":4,        #红卡
"GD_BT":5,      #金币抽卡
"DM_BT":6,      #钻石抽卡
"TS":7,         #天使
"GDF":8,        #甘道夫
"WZJ":9,        #王昭君
"BWC":10,       #白无常
"money_box":11,   #金币框
"city_bt":12,      #回城键
"trans_page":13,   #传送页面
"death_bt":14,     #死亡按钮
"box_page":15     #宝箱页面
"""
model = YOLO("./card_best.pt")  # load a custom model

class Hero:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.hwnd = 0
        self.get_hwnd()

        self.flag = True

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
    def do_click(self, position_x, position_y):
        self.get_hwnd()
        # 宏 
        long_position = win32api.MAKELONG(int(position_x), int(position_y))
        #鼠标左键按下
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN,0,long_position)
        # time.sleep(0.05)
        self.my_time_sleep(0.05)
        #鼠标左键抬起
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP,0,long_position)

    #控制人物移动
    def move(self, dir, move_time):
        if self.flag == True:
            self.get_hwnd()
            w = self.w
            h = self.h
            x0 = int(0.5*self.w)
            y0 = int(0.785*self.h)
            lp = win32api.MAKELONG(x0, y0)

            px, py = 0,0
            if   dir == 'w':
                px, py = x0 , y0-0.3*w
            elif dir == 'a':
                px, py = x0-0.3*w , y0
            elif dir == 's':
                px, py = x0 , y0+0.3*w
            elif dir == 'd':
                px, py = x0+0.3*w , y0
            elif dir == 'wa'or dir == 'aw':
                px, py = x0-0.3*w, y0-0.3*w/h*w
            elif dir == 'wd' or dir == 'dw':
                px, py = x0+0.3*w , y0-0.3*w/h*w
            elif dir == 'sa'or dir == 'as':
                px, py = x0-0.3*w , y0+0.3*w/h*w
            elif dir == 'sd'or dir == 'ds':
                px, py = x0+0.3*w , y0+0.3*w/h*w
            
            lp2 = win32api.MAKELONG(int(px),int(py))
            #鼠标按下lp位置
            self.do_click(0.5*w, 0.98*h)
            self.my_time_sleep(0.02)
            win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, lp)
            #鼠标移动到 lp2位置
            self.my_time_sleep(0.02)
            win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, lp2)
            #鼠标保持时间
            self.my_time_sleep(move_time)
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
    def my_time_sleep(self,sleep_time):
        t = time.time()
        while self.flag:
            if time.time() - t > sleep_time:
                return 0
            
    #后台截图
    def capture(self):
        if self.flag == True:
            hwnd_dc = win32gui.GetWindowDC(self.hwnd)
            mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
            save_dc = mfc_dc.CreateCompatibleDC()
            bitmap = win32ui.CreateBitmap()
            bitmap.CreateCompatibleBitmap(mfc_dc, self.w, self.h)
            save_dc.SelectObject(bitmap)

            windll.user32.PrintWindow(self.hwnd, save_dc.GetSafeHdc(), 3)

            bmpinfo = bitmap.GetInfo()
            bmpstr = bitmap.GetBitmapBits(True)
            img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
            img = img[:,:,:3]

            
            win32gui.DeleteObject(bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwnd_dc)
            return img

    def yolo_det(self,class_type):
        img = self.capture()
        results = model(img)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # 获取类别名称
                class_name = model.names[int(box.cls)]
                if class_name == class_type:
                    # 获取边界框坐标
                    bbox = box.xywh[0]
                    return bbox[0], bbox[1]
                    





if __name__ == "__main__":
    p = Hero()
    # # print(p.hwnd)
    # # p.do_click(333/610*p.w,421/1113*p.h,1)
    # p.disable_mouse_input()
    # p.move("a",0)
    # p.move("w",5)
    # p.enable_mouse_input()

    # img = p.capture()
    # cv2.imshow("imgshow", img)
    # cv2.waitKey(0)

    x,y = p.yolo_det("fdj")
    p.do_click(x,y)


    

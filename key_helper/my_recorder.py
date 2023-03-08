import os, time
import threading
import json
#import pyautogui
from datetime import datetime
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyController, KeyCode
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from Ui_mouse_recorder import *
from my_window import *


RECORD_KEY = Key.f9
PLAY_KEY = Key.f10
CON_CLICK_KEY = Key.f8

command_list=[]

BUTTONS = {
        "Button.left": Button.left,
        "Button.right": Button.right,
        "Button.middle": Button.middle
}

class MyRecorder(QObject):
    refresh = pyqtSignal(str)
    minimized = pyqtSignal()
    active = pyqtSignal()
    savefile = pyqtSignal()
    showstatus = pyqtSignal(str)
    def __init__(self, Window=None):
        super().__init__()
        self.__window = Window
        self.__record_flag = False
        self.__conclick_flag = False
        self.__play_flag = False
        self.__key_thread = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.__key_thread.start()
        self.__mouse_thread = mouse.Listener(on_click=self.on_click)
        self.__mouse_thread.start()

    def on_click(self, x, y, button, pressed):
        if self.__record_flag:
            timestr= datetime.now().strftime("%Y_%m_%d_%H_%M_%S.%f")[:-3]
            print(timestr, x, y, pressed, button)
            command_list.append((
                "mouse", #opration object
                (x, y, pressed, str(button)),
                timestr
            ))
    
    def on_press(self, key):
        if key == CON_CLICK_KEY or key == RECORD_KEY or key == PLAY_KEY:
            print("press key", key)
        else:
            if self.__record_flag:
                self.record_key(key, True) #True or False for press or release

    def on_release(self, key):
        print("release key", key)
        if key == CON_CLICK_KEY or key == RECORD_KEY or key == PLAY_KEY:
            self.handle_key(key)#do nothing when press function keys
        else:
            if self.__record_flag:
                self.record_key(key, False)

    def handle_key(self, key):
        if key == CON_CLICK_KEY:
            self.handle_conclick()
        elif key == RECORD_KEY:
            self.handle_record()
        elif key == PLAY_KEY:
            self.handle_play()
        else:
            print("error key")

    def continuous_click(self):
        interval = self.__window.timeinterval_lineEdit.text()
        print("interval", interval)
        if interval == "": #if no numbers, default to 1s
            interval = 1
        interval = float(interval)
        #self.__window.setWindowState(Qt.WindowMinimized)
        mouse = MouseController()
        while self.__conclick_flag:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            mouse.click(button=Button.left)
            print("continuous click key")
            time.sleep(interval)

    def handle_conclick(self):
        global mouse_click_thread
        if self.__conclick_flag:
            self.__conclick_flag = False
            mouse_click_thread.join()
            if not mouse_click_thread.is_alive():
                mouse_click_thread = None
            self.showstatus.emit("当前状态:\n鼠标左键连点结束...")
            self.active.emit()
            #self.__window.setWindowState(Qt.WindowActive)
        else:
            self.__conclick_flag = True
            #create new threading everytime
            #self.__window.setWindowState(Qt.WindowMinimized)
            mouse_click_thread = threading.Thread(target=self.continuous_click)
            mouse_click_thread.start()
            self.showstatus.emit("当前状态:\n鼠标左键连点中...")
            self.minimized.emit()

    def handle_record(self):
        print(self.__record_flag)
        if self.__record_flag:
            print("stop recording")
            self.__record_flag = False
            self.showstatus.emit("当前状态:\n鼠标键盘录制结束...")
            self.active.emit()
            self.savefile.emit()
            #self.__window.setWindowState(Qt.WindowActive)
            #get current path
            #cwdpath = os.getcwd()
            #print("current path" + cwdpath)
            #create or enter scripts path
            #scriptspath = cwdpath + "\scripts\\"
            #filename = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())) + "_Record.json"
            #path = scriptspath + filename
            #print(path)
            #self.tofile(command_list, path)
            #self.refresh.emit(filename)
        else:
            #self.__window.setWindowState(Qt.WindowMinimized)
            self.showstatus.emit("当前状态:\n鼠标键盘录制中...")
            self.minimized.emit()
            print("start recording")
            self.__record_flag = True
            print("flag", self.__record_flag)

    def handle_play(self):
        global record_play_thread
        if self.__play_flag:
            self.__play_flag = False
            print("play flag", self.__play_flag)
            record_play_thread.join()
            if record_play_thread.is_alive():
                record_play_thread = None
            self.showstatus.emit("当前状态:\n鼠标键盘播放结束...")
            self.active.emit()
        else:
            self.__play_flag = True
            #self.__window.setWindowState(Qt.WindowMinimized)
            record_play_thread = threading.Thread(target=self.do_play)
            record_play_thread.start()
            self.showstatus.emit("当前状态:\n鼠标键盘播放中...")
            self.minimized.emit()
    
    def do_play(self):
        filepath = self.__window.get_current_filepath()
        print(filepath)
        if filepath == []:
            return
        command_read = []
        with open(filepath, encoding='utf-8-sig', errors='ignore') as f:
            command_read = json.loads(f.read())
        
        while True:
            print("do play")
            old_timestamp = 0
            timestamp = 0
            i = 0
            for command in command_read:
                print("one command start", i)
                print("oldtimestamp", old_timestamp)
                timestr = command[2]
                print("timestr", timestr)
                timestamp = datetime.strptime(timestr, "%Y_%m_%d_%H_%M_%S.%f").timestamp()
                print("timestamp", timestamp)
                if old_timestamp !=0:
                    timedelay = timestamp - old_timestamp
                    print("delay", timedelay)
                    time.sleep(timedelay)
                    if not self.__play_flag:
                        break
                old_timestamp = timestamp
                if command[0] == "mouse":
                    mouse = MouseController()
                    paser = command[1]
                    x = paser[0]
                    y = paser[1]
                    pressed = paser[2]
                    value = paser[3]
                    print("mouse play", x, y, value, pressed, timestr)
                    #pyautogui.moveTo(x,y)
                    mouse.position = (x,y)
                    if pressed:
                        mouse.press(button=BUTTONS[value])
                    else:
                        mouse.release(button=BUTTONS[value])
                elif command[0] == "keyboard":
                    keycon= KeyController()
                    paser = command[1]
                    pressed = paser[2]
                    value = paser[3]
                    if value[:3] == "Key":
                        key = eval(value, {}, {"Key": keyboard.Key})
                    else:
                        key = value
                    #value = "Key." + value.replace('\'','')
                    print(value, pressed, timestr)
                    #key = getattr(KeyCode, value)
                    if pressed:
                        keycon.pressed(key)
                    else:
                        keycon.release(key)
                    print("keyboard play", key, pressed)           
                else:
                    print("incorrect mode")
                i = i + 1
                if not self.__play_flag:
                    break
            print("self.__play_flag", self.__play_flag)
            if not self.__play_flag:
                break
            interval = self.__window.timeinterval_lineEdit.text()
            print("interval", interval)
            if interval == "": #if no numbers, default to 1s
                interval = 1
            interval = float(interval)
            time.sleep(interval)

    def record_key(self, key, pressed):
        timestr= datetime.now().strftime("%Y_%m_%d_%H_%M_%S.%f")[:-3]
        print(timestr, pressed, key)
        command_list.append((
            "keyboard", #opration object
            (-1, -1, pressed, str(key).strip("'")),
            timestr
        ))

    def getcommandlist(self):
        return command_list

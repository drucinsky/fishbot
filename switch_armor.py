import pyautogui
import keyboard
from PyQt5.QtCore import QObject, QThread, pyqtSignal

class SwitchArmor(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    arm_start_x, arm_start_y = 0, 0


    def setArmorCords(self):
        mouse_position = None
        self.progress.emit("Najedź na zbroję i kliknij 'r'")
        while mouse_position is None:
            if keyboard.is_pressed('r'):
                mouse_position = pyautogui.position()

        self.arm_start_x, self.arm_start_y = mouse_position[0], mouse_position[1]
        self.finished.emit()

    def ppm_click_on_armor(self):
        pyautogui.click(self.arm_start_x, self.arm_start_y, button='right')

    def show_armor_position(self):
        pyautogui.moveTo(self.arm_start_x, self.arm_start_y, duration=0)

from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time
import keyboard
import fishing_area
import switch_armor

class BotStart(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    aplicationRunning = pyqtSignal(bool)
    running = False

    def __init__(self, fishing_area, armorClass):
        super().__init__()
        self.fishing_area_class = fishing_area
        self.armor_class = armorClass

    def startBot(self):
        self.running = True
        self.armorChange = switch_armor.SwitchArmor()
        clickCounter = 0 
        print(self.armorChange.arm_start_x)
        if self.armorChange.arm_start_x != 0:
            self.armorChange.ppm_click_on_armor()
            
        keyboard.press('4')
        time.sleep(0.5)
        keyboard.press('space')

        while self.running:
            self.aplicationRunning.emit(True)
            self.progress.emit(str(clickCounter))
            if clickCounter <= 3:
                fish_position = self.fishing_area_class.getFishInAreaZone()
                self.fishing_area_class.clickInFish(fish_position)
                clickCounter += 1
                time.sleep(1.3)
            else:
                clickCounter = 0
                self.progress.emit('Reset')
                if self.armorChange.arm_start_x != 0:
                    self.armorChange.ppm_click_on_armor()
                else:
                    time.sleep(5)
                keyboard.press('4')
                time.sleep(0.5)
                keyboard.press('space')
                time.sleep(0.1)

        self.progress.emit('Nie działam')
        self.finished.emit()

    def stopBot(self):
        self.aplicationRunning.emit(False)
        self.running = False
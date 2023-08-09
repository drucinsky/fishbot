import keyboard
import pyautogui
from PIL import ImageGrab
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time

class FishingArea(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    fishing_area_start_x, fishing_area_start_y, fishing_area_end_x, fishing_area_end_y = 0, 0, 0, 0
    image_area_zone = None

    def setFishingAreaCorners(self):
        left_corner = None
        right_corner = None
        is_waiting_for_left_corner = True
        self.progress.emit("Aby wyznaczyć obszar łowienia, daj kursor na lewy górny róg obszaru łowienia i kliknij 'l'")
        while left_corner is None:
            if is_waiting_for_left_corner:
                time.sleep(0.1)
                if keyboard.is_pressed('l'):
                    left_corner = pyautogui.position()
                    is_waiting_for_left_corner = False
                    self.progress.emit("Gotowe, teraz wyznacz prawy dolny róg i kliknij 'r'")


        while right_corner is None:
            time.sleep(0.1)
            if keyboard.is_pressed('r'):
                right_corner = pyautogui.position()

        self.fishing_area_start_x, self.fishing_area_start_y, self.fishing_area_end_x, self.fishing_area_end_y = left_corner[0], left_corner[1], right_corner[0], right_corner[1]
        self.setImageZone()
        self.finished.emit()

    
    def getFishingAreaCord(self):
        return (self.fishing_area_start_x, self.fishing_area_start_y, self.fishing_area_end_x, self.fishing_area_end_y)
    
    def showFishingZone(self):
        if self.fishing_area_start_x == 0:
            return
        #img = ImageGrab.grab(self.getFishingAreaCord())
        self.image_area_zone.show()

    def setImageZone(self):
        self.image_area_zone = ImageGrab.grab(bbox=self.getFishingAreaCord())

    def getFishInAreaZone(self, threshold=10):
        color = (55, 89, 122)
        fishCord = None
        while fishCord is None:
            self.setImageZone()
            for x in range(self.image_area_zone.width):
                for y in range(self.image_area_zone.height):
                    pixel_color = self.image_area_zone.getpixel((x, y))
                    if all(abs(pixel_color[i] - color[i]) <= threshold for i in range(3)):
                        fishCord = (x + self.fishing_area_start_x, y + self.fishing_area_start_y)
                        break
                
        return fishCord
    
    def clickInFish(self, position):
        pyautogui.click(position[0], position[1], button='left')

                

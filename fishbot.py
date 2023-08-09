import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import main_window
import fishing_area
import switch_armor
import bot_start

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main_window.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.btn_select_fishing_area.clicked.connect(self.detect_fishing_area)
        self.ui.btn_change_armor.clicked.connect(self.detect_armor_area)
        self.ui.preview_fishing_zone.clicked.connect(self.show_fishing_zone)
        self.ui.preview_armor_zone.clicked.connect(self.show_armor_zone)
        self.ui.btn_start.clicked.connect(self.start_bot)

        self.bot_is_run = False
    
    def detect_fishing_area(self):
        # Step 1: Create a QThread object
        self.thread = QThread()
        self.fishingAreaClass = fishing_area.FishingArea()
        # Step 2: Move fishingAreaClass to the thread
        self.fishingAreaClass.moveToThread(self.thread)
        # Step 3: Connect signals and slots
        self.thread.started.connect(self.fishingAreaClass.setFishingAreaCorners)
        self.thread.finished.connect(self.thread.deleteLater)
        self.fishingAreaClass.progress.connect(self.report_progress)
        self.fishingAreaClass.finished.connect(self.thread.quit)
        self.fishingAreaClass.finished.connect(self.fishingAreaClass.deleteLater)
        # Step 4: Start the thread
        self.thread.start()
        # Final resets
        self.ui.btn_select_fishing_area.setEnabled(False)

        self.thread.finished.connect(
            lambda: self.ui.btn_select_fishing_area.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.ui.label_information.setText("Obszar łowienia wyznaczony")
        )

    def detect_armor_area(self):
         # Step 1: Create a QThread object
        self.thread = QThread()
        self.switchArmorClass = switch_armor.SwitchArmor()
        # Step 2: Move fishingAreaClass to the thread
        self.switchArmorClass.moveToThread(self.thread)
        # Step 3: Connect signals and slots
        self.thread.started.connect(self.switchArmorClass.setArmorCords)
        self.thread.finished.connect(self.thread.deleteLater)
        self.switchArmorClass.progress.connect(self.report_progress)
        self.switchArmorClass.finished.connect(self.thread.quit)
        self.switchArmorClass.finished.connect(self.switchArmorClass.deleteLater)
        # Step 4: Start the thread
        self.thread.start()
        # Final resets
        self.ui.btn_change_armor.setEnabled(False)

        self.thread.finished.connect(
            lambda: self.ui.btn_change_armor.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.ui.label_information.setText("Pozycja zbroi do zmiany wyznaczona")
        )

    def start_bot(self):
        if self.bot_is_run:
            self.bot_is_run = False
            self.startBotClass.stopBot()

        else:
            self.bot_is_run = True
            self.ui.btn_start.setText("Start")
            self.thread = QThread()
            self.startBotClass = bot_start.BotStart(self.fishingAreaClass, self.switchArmorClass)
            # Step 2: Move fishingAreaClass to the thread
            self.startBotClass.moveToThread(self.thread)
            # Step 3: Connect signals and slots
            self.thread.started.connect(self.startBotClass.startBot)
            self.thread.finished.connect(self.thread.deleteLater)
            self.startBotClass.progress.connect(self.report_progress)
            self.startBotClass.aplicationRunning.connect(self.application_runing)
            self.startBotClass.finished.connect(self.thread.quit)
            self.startBotClass.finished.connect(self.startBotClass.deleteLater)
            # Step 4: Start the thread
            self.thread.start()

    def application_runing(self, value):
        if value:
            self.ui.btn_start.setText("Stop")
            self.ui.btn_select_fishing_area.setEnabled(False)
            self.ui.btn_change_armor.setEnabled(False)
        else:
            self.ui.btn_start.setText("Start")
            self.ui.btn_select_fishing_area.setEnabled(True)
            self.ui.btn_change_armor.setEnabled(True)

    def show_fishing_zone(self):
        self.fishingAreaClass.showFishingZone()

    def show_armor_zone(self):
        self.switchArmorClass.ppm_click_on_armor()

    def report_progress(self, value):
        self.ui.label_information.setText(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
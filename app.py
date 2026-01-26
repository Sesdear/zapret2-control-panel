import npyscreen
from src.froms.mainform import MainForm
from src.froms.configform import ConfigForm
from src.froms.unknown import Unknown
from src.froms.serviceform import ServiceForm
from src.froms.changestrategyform import ChangeStrategyForm
from src.froms.manualstrategy import ManualChangeStrategy
import os, sys

import npyscreen
import sys
import fcntl
import struct
import termios
import os

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainForm, name="Zapret2 Control Panel")
        self.addForm('CONFIG', ConfigForm, name="Zapret2 Control Panel - Configuration")
        self.addForm('SERVICE', ServiceForm, name="Zapret2 Control Panel - Service Management")
        self.addForm('CHANGEIPSET', Unknown, name="Configuration - Change IP Set (Coming Soon)")
        self.addForm('CHANGESTRATEGY', ChangeStrategyForm, name="Configuration - Change Strategy")
        self.addForm('MANUALSTRATEGY', ManualChangeStrategy, name="Configuration - Manual Strategy Selection")
        
        self.addForm('UNKNOWN', Unknown, name="Zapret2 Control Panel - Coming Soon")
        
        
if __name__ == '__main__':
    if os.geteuid() != 0:
        print("Запуск возможен только от root")
        sys.exit(1)
    app = App()
    app.run()
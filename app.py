import npyscreen
from src.froms.mainform import MainForm
from src.froms.configform import ConfigForm
from src.froms.unknown import Unknown
from src.froms.serviceform import ServiceForm
from src.froms.changestrategyform import ChangeStrategyForm

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainForm, name="Zapret2 Control Panel")
        self.addForm('CONFIG', ConfigForm, name="Zapret2 Control Panel - Configuration")
        self.addForm('SERVICE', ServiceForm, name="Zapret2 Control Panel - Service Management")
        self.addForm('CHANGEIPSET', Unknown, name="Configuration - Change IP Set (Coming Soon)")
        self.addForm('CHANGESTRATEGY', ChangeStrategyForm, name="Configuration - Change Strategy")
        
        self.addForm('UNKNOWN', Unknown, name="Zapret2 Control Panel - Coming Soon")
        
        
if __name__ == '__main__':
    app = App()
    app.run()
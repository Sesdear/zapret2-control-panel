import npyscreen
import os
import json

class ConfigForm(npyscreen.FormBaseNew):
    def create(self):
        self.current_config = ""
        if not os.path.exists("/opt/zapret2-installer/data/config.json") or os.path.getsize("/opt/zapret2-installer/data/config.json") == 0:
            self.current_config = "Unknown"
        else:
            with open("/opt/zapret2-installer/data/config.json", "r") as f:
                _data = json.load(f)
            self.current_config = _data.get("strategy", "Unknown")
            
    
        self.add(npyscreen.TitleText, name=f"Текущая конфигурация: {self.current_config}", editable=False)
        self.add(npyscreen.ButtonPress, name="Сменить стратегию", when_pressed_function=self.change_strategy)
        self.add(npyscreen.ButtonPress, name="Сменить лист обхода", when_pressed_function=self.change_ipset)
        self.add(npyscreen.ButtonPress, name="Назад в меню", when_pressed_function=self.back_to_main)

    def unknown_function(self):
        self.parentApp.switchForm('UNKNOWN')

    def change_ipset(self):
        self.parentApp.switchForm('CHANGEIPSET')
    
    def change_strategy(self):
        self.parentApp.switchForm('CHANGESTRATEGY')
    
    def back_to_main(self):
        self.parentApp.switchForm('MAIN')
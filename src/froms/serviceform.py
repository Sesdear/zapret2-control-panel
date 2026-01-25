import npyscreen
from src.utils.service_actions import ServiceActions

class ServiceForm(npyscreen.FormBaseNew):
    def create(self):

        if ServiceActions.check_zapret_auto_start() == "enabled":
            self.zapret_auto_start_status = "Отключить автозапуск"
        else:
            self.zapret_auto_start_status = "Включить автозапуск"
        
        self.add(npyscreen.ButtonPress, name=self.zapret_auto_start_status, when_pressed_function=ServiceActions.toggle_zapret_auto_start)
        self.add(npyscreen.FixedText, value="")
        self.add(npyscreen.ButtonPress, name="Назад в меню", when_pressed_function=self.back_to_main)
    
    def back_to_main(self):
        self.parentApp.switchForm('MAIN')
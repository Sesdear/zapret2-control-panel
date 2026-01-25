import npyscreen
from src.utils.service_actions import ServiceActions

class MainForm(npyscreen.FormBaseNew):
    
    def create(self):
                
        status = ServiceActions.check_zapret_service()
        
        if status == "active":
            self.zapret_status = "Выключить"
        else:
            self.zapret_status = f"Включить"
        
        self.service_status_title = self.add(npyscreen.TitleFixedText, 
                name="Статус сервиса:", 
                value=status, 
                editable=False)
        
        self.service_button = self.add(npyscreen.ButtonPress, 
                name=self.zapret_status, 
                when_pressed_function=self.toggle_service)
        
        self.add(npyscreen.ButtonPress, name="Настройка конфигурации", when_pressed_function=self.call_config_form)
        self.add(npyscreen.ButtonPress, name="Настройка сервиса", when_pressed_function=self.call_service_form)
        self.add(npyscreen.ButtonPress, name="Проверить на наличие обновлений", when_pressed_function=self.unknown_function)
        self.add(npyscreen.FixedText, value="")
        self.add(npyscreen.ButtonPress, name="Выйти", when_pressed_function=self.exit_application)
        self.add(npyscreen.TitleText, name="\n\nCreated by sesdear.github.io", editable=False)

    def toggle_service(self):
        result = ServiceActions.toggle_zapret_service()

        if result.startswith("error"):
            npyscreen.notify_confirm(
                f"Ошибка: {result}",
                title="Ошибка"
            )
            return

        status = ServiceActions.check_zapret_service()

        if status == "active":
            self.service_button.name = "Выключить"
        else:
            self.service_button.name = "Включить"

        self.service_status_title.value = status

        self.service_button.display()
        self.service_status_title.display()


    def unknown_function(self):
        self.parentApp.switchForm('UNKNOWN')
        
    def call_service_form(self):
        self.parentApp.switchForm('SERVICE')

    def call_config_form(self):
        self.parentApp.switchForm('CONFIG')

    def exit_application(self):
        exit()
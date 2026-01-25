import npyscreen
import subprocess

class MainForm(npyscreen.FormBaseNew):
    
    def create(self):
                
        if self.check_zapret_service() == "active":
            self.zapret_status = "Выключить zapret2"
        else:
            self.zapret_status = "Включить zapret2"
        
        self.add(npyscreen.TitleText, name=f"Статус Zapret: {self.check_zapret_service()}", editable=False)
        
        self.add(npyscreen.ButtonPress, name=self.zapret_status, when_pressed_function=self.toggle_zapret_service)
        self.add(npyscreen.ButtonPress, name="Настройка конфигурации", when_pressed_function=self.call_config_form)
        self.add(npyscreen.ButtonPress, name="Настройка сервиса", when_pressed_function=self.call_service_form)
        self.add(npyscreen.ButtonPress, name="Проверить на наличие обновлений", when_pressed_function=self.unknown_function)
        self.add(npyscreen.ButtonPress, name="Выйти", when_pressed_function=self.exit_application)
        self.add(npyscreen.TitleText, name="\n\nCreated by sesdear.github.io", editable=False)

    def unknown_function(self):
        self.parentApp.switchForm('UNKNOWN')
        
    def call_service_form(self):
        self.parentApp.switchForm('SERVICE')

    def call_config_form(self):
        self.parentApp.switchForm('CONFIG')

    def check_zapret_service(self) -> str:
        try:
            result = subprocess.run(['systemctl', 'is-active', 'zapret2'], capture_output=True, text=True, check=True)
            status = result.stdout.strip()
            if status == 'active':
                return "active"
            else:
                return "inactive"
        except subprocess.CalledProcessError:
            return "inactive: error"
        
    def toggle_zapret_service(self):
        current_action = self.check_zapret_service()
        try:
            if current_action == "Выключить":
                subprocess.run(['sudo', 'systemctl', 'stop', 'zapret2'], check=True)
            else:
                subprocess.run(['sudo', 'systemctl', 'start', 'zapret2'], check=True)
        except subprocess.CalledProcessError as e:
            npyscreen.notify_confirm(f"Ошибка при изменении состояния сервиса: {e}", title="Ошибка")
        self.check_zapret_service()
        self.parentApp.switchForm('SERVICE')

    def exit_application(self):
        exit()
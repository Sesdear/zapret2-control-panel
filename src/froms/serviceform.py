import npyscreen
import subprocess

class ServiceForm(npyscreen.FormBaseNew):
    def create(self):

        if self.check_zapret_auto_start() == "enabled":
            self.zapret_auto_start_status = "Отключить автозапуск"
        else:
            self.zapret_auto_start_status = "Включить автозапуск"
        
        self.add(npyscreen.ButtonPress, name=self.zapret_auto_start_status, when_pressed_function=self.change_zapret_auto_start)
        
        self.add(npyscreen.ButtonPress, name="Назад в меню", when_pressed_function=self.back_to_main)

    def change_zapret_auto_start(self):
        current_action = self.check_zapret_auto_start()
        try:
            if current_action == "enabled":
                subprocess.run(['sudo', 'systemctl', 'disable', 'zapret2'], check=True)
            else:
                subprocess.run(['sudo', 'systemctl', 'enable', 'zapret2'], check=True)
        except subprocess.CalledProcessError as e:
            npyscreen.notify_confirm(f"Ошибка при изменении автозапуска: {e}", title="Ошибка")
        self.check_zapret_auto_start()
        self.parentApp.switchForm('SERVICE')

    def check_zapret_auto_start(self) -> str:
        try:
            result = subprocess.run(['systemctl', 'is-enabled', 'zapret2'], capture_output=True, text=True, check=True)
            status = result.stdout.strip()
            if status == 'enabled':
                return "enabled"
            else:
                return "disabled"
        except subprocess.CalledProcessError:
            return "disabled: error"

    
    def back_to_main(self):
        self.parentApp.switchForm('MAIN')
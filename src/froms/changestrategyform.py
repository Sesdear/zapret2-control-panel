import npyscreen

class ChangeStrategyForm(npyscreen.FormBaseNew):
    def create(self):

        self.add(npyscreen.ButtonPress, name="Выбрать в ручную", when_pressed_function=self.back_to_config)
        self.add(npyscreen.ButtonPress, name="Автоматический подбор стратегии", when_pressed_function=self.back_to_config)
        self.add(npyscreen.ButtonPress, name="Назад в настройки", when_pressed_function=self.back_to_config)

    
    def manual_selection(self):
        self.parentApp.switchForm('UNKNOWN')
        
    def auto_selection(self):
        self.parentApp.switchForm('UNKNOWN')
    
    
    def back_to_config(self):
        self.parentApp.switchForm('CONFIG')
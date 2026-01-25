import npyscreen

class ManualChangeStrategy(npyscreen.FormBaseNew):
    def create(self):

        self.add(npyscreen.TitleText, name="Ручной выбор стратегии (Coming Soon)", editable=False)
        self.add(npyscreen.ButtonPress, name="Назад в настройки", when_pressed_function=self.back_to_config)

    def back_to_config(self):
        self.parentApp.switchForm('CONFIG')
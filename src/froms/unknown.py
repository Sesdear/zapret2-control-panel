import npyscreen

class Unknown(npyscreen.FormBaseNew):
    
    def create(self):
        self.add(npyscreen.TitleText, name="Coming soon...", editable=False)
        self.add(npyscreen.ButtonPress, name="Назад в меню", when_pressed_function=self.back_to_main)

    def back_to_main(self):
        self.parentApp.switchForm('MAIN')
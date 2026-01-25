import npyscreen
from src.utils.configs_list import ConfigsList
from src.utils.apply_strategy import ApplyStrategy

class ManualChangeStrategy(npyscreen.FormBaseNew):
    def create(self):

        configs = ConfigsList.fetch_configs()
        
        text_lines = [f"{i}. {config}" for i, config in enumerate(configs, start=1)]
        self.add(npyscreen.MultiLineEdit,
                value="\n".join(text_lines),
                editable=False,
                max_height=len(configs))
        
        self.strategy_num = self.add(npyscreen.TitleText, 
                                    name="Номер стратегии (1-{0}):".format(len(configs)),
                                    editable=True)
        self.add(npyscreen.ButtonPress, name="Подтвердить", when_pressed_function=self.apply_strategy)
        self.add(npyscreen.FixedText, value="", editable=False)
        self.add(npyscreen.ButtonPress, name="Назад в настройки", when_pressed_function=self.back_to_config)

    def apply_strategy(self):
        
        selected_index = int(self.strategy_num.value) - 1
        configs = ConfigsList.fetch_configs()
        
        if 0 <= selected_index < len(configs):
            
            selected_strategy = configs[selected_index]
            
            if ApplyStrategy.requires_root():
                npyscreen.notify_confirm("Для применения стратегии требуются права суперпользователя (root). Пожалуйста, запустите программу с правами root.", title="Ошибка прав доступа")
                return
            
            ApplyStrategy.apply_strategy(selected_strategy)
            
            npyscreen.notify_confirm(f"Стратегия '{selected_strategy}' успешно применена.", title="Успех")
            self.parentApp.switchForm('CONFIG')
            
        else:
            
            npyscreen.notify_confirm("Неверный номер стратегии. Пожалуйста, попробуйте снова.", title="Ошибка")

    def back_to_config(self):
        self.parentApp.switchForm('CONFIG')
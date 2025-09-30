# """
# This module for Dariya's work, GUI maker.
# """
# import tkinter as tk
#
# def click():
#     create.config(text="Сработало")
#
# window = tk.Tk()
# window.title("Главная")
# window.geometry("500x300")
#
# create = tk.Label(window, text="", font=("Arial", 16))
# create.pack(pady=40)
#
# button = tk.Button(window, text="Тыкни", command=click)
# button.pack(pady=10)
#
# window.mainloop()
#
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox


class SimpleApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Список тегов
        self.tags = ['Право', 'Обязательство', 'Реквизиты', 'Аннулирование', 'Продление']
        self.selected_tags = []

        # Кнопка выбора тегов
        self.select_btn = Button(
            text='Выбрать теги',
            size_hint=(1, 0.2),
            background_color=(0.3, 0.3, 0.5, 1)
        )
        self.select_btn.bind(on_press=self.show_tags)
        self.layout.add_widget(self.select_btn)

        # Метка выбранных тегов
        self.tags_label = Label(
            text='Теги не выбраны',
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.tags_label)

        # Кнопка старта
        self.start_btn = Button(
            text='Старт',
            size_hint=(1, 0.2),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        self.start_btn.bind(on_press=self.start)
        self.layout.add_widget(self.start_btn)

        return self.layout

    def show_tags(self, instance):
        popup_layout = BoxLayout(orientation='vertical', spacing=10)

        # Добавляем чекбоксы для тегов
        self.checkboxes = {}
        for tag in self.tags:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            checkbox = CheckBox(active=tag in self.selected_tags)
            label = Label(text=tag)

            self.checkboxes[tag] = checkbox
            row.add_widget(checkbox)
            row.add_widget(label)
            popup_layout.add_widget(row)

        # Кнопки управления
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        apply_btn = Button(text='Применить')
        apply_btn.bind(on_press=self.apply_tags)

        cancel_btn = Button(text='Отмена')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())

        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(apply_btn)
        popup_layout.add_widget(btn_layout)

        popup = Popup(
            title='Выберите теги',
            content=popup_layout,
            size_hint=(0.7, 0.8)
        )

        self.popup = popup
        popup.open()

    def apply_tags(self, instance):
        self.selected_tags = []

        for tag, checkbox in self.checkboxes.items():
            if checkbox.active:
                self.selected_tags.append(tag)

        # Обновляем метку
        if self.selected_tags:
            self.tags_label.text = f'Теги: {", ".join(self.selected_tags)}'
        else:
            self.tags_label.text = 'Теги не выбраны'

        self.popup.dismiss()

    def start(self, instance):
        if self.selected_tags:
            print(f"Запуск с тегами: {', '.join(self.selected_tags)}")
        else:
            print("Запуск без тегов")


if __name__ == '__main__':
    SimpleApp().run()
<<<<<<< Updated upstream
"""
This module for Dariya's work, GUI maker.
"""
=======
import tkinter as tk

def click():
    create.config(text="Сработало")

window = tk.Tk()
window.title("Главная")
window.geometry("500x300")

create = tk.Label(window, text="", font=("Arial", 16))
create.pack(pady=40)

button = tk.Button(window, text="Тыкни", command=click)
button.pack(pady=10)

window.mainloop()
>>>>>>> Stashed changes

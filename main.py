import customtkinter
from PIL import Image, ImageFilter
import os
from bd.bd import check_login

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    width = 1000
    height = 600

    def login_event(self):
        input_key = self.key_entry.get()
        chk = check_login(input_key)

        if chk == True:
            self.login_frame.grid_forget()  # remove login frame
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show main frame

    def checkbox_event_inactive(self):
        if self.checkbox_1:
            self.key_entry = customtkinter.CTkEntry(self.login_frame, width=500, show="*", placeholder_text="Key")
            self.key_entry.place(relx=0.5, rely=0.5, anchor="center")

            self.checkbox_1.configure(command=self.checkbox_event_active)
        # Обновляем отображение поля ввода
        self.key_entry.update()

    def checkbox_event_active(self):
        if self.checkbox_1:
            self.key_entry = customtkinter.CTkEntry(self.login_frame, width=500, placeholder_text="Key")
            self.key_entry.place(relx=0.5, rely=0.5, anchor="center")

            self.checkbox_1.configure(command=self.checkbox_event_inactive)
        # Обновляем отображение поля ввода
        self.key_entry.update()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Skywalker")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(
            Image.open(current_path + "/test_images/bg_gradient.jpg").filter(ImageFilter.BLUR),
            size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="nsew", padx=70, pady=70)

        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Авторизация",
                                                  font=customtkinter.CTkFont(size=30, weight="bold"))
        self.login_label.place(relx=0.5, rely=0.2, anchor="center")

        # Создание объекта key
        self.key_entry = customtkinter.CTkEntry(self.login_frame, width=500, show="*", placeholder_text="Key")
        self.key_entry.place(relx=0.5, rely=0.5, anchor="center")

        # Создание объекта checkbox
        self.checkbox_1 = customtkinter.CTkCheckBox(self.login_frame, text="Показать", command=self.checkbox_event_active)
        self.checkbox_1.place(relx=0.87, rely=0.5, anchor="center")

        # Кнопка
        login_button_font = customtkinter.CTkFont(size=15)
        self.login_button = customtkinter.CTkButton(self.login_frame, corner_radius=10, text="LOGIN", command=self.login_event, width=400, height=50, font=login_button_font)
        self.login_button.place(relx=0.5, rely=0.8, anchor="center")

        # create main frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.main_label = customtkinter.CTkLabel(self.main_frame, text="CustomTkinter\nMain Page",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.main_label.grid(row=0, column=0)

if __name__ == "__main__":
    app = App()
    app.mainloop()

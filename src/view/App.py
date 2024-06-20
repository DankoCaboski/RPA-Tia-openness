import customtkinter
from components.Button import CustomButton


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x180")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        custom_button = CustomButton(self, "Meu botão", command=self.button_callback)  # Create an instance of CustomButton
        button = custom_button()  # Call the instance to create the button
        button.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")  # Add the button to the grid

    def button_callback(self):
        print("button pressed")

app = App()
app.mainloop()
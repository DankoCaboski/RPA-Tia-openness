import customtkinter

from view.components.CustomCheckbox import CustomCheckbox
from view.components.CustomButton import CustomButton

from view.functions.ButtonHandler import ButtonHandler


class App(customtkinter.CTk):
    
    callback_handler = ButtonHandler()
    
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x180")
        self.iconbitmap("view/assets/favico.ico")

        inst_custom_checkbox_1 = CustomCheckbox(self, "Checkbox 1")  # Create an instance of CustomCheckbox
        checkbox_1 = inst_custom_checkbox_1()  # Call the instance to create the checkbox
        checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")  # Add the checkbox to the grid
        
        inst_custom_checkbox_2 = CustomCheckbox(self, "Checkbox 2")
        checkbox_2 = inst_custom_checkbox_2()
        checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        custom_button = CustomButton(self, "Meu botão", command=self.callback_handler.button_callback)  # Create an instance of CustomButton
        button = custom_button()  # Call the instance to create the button
        button.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")  # Add the button to the grid


app = App()
app.mainloop()
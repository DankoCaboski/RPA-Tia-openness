from CustomTkinter import customtkinter


class CustomCheckbox:
    def __init__(self, frame, texto):
        self.frame = frame
        self.texto = texto

    def __call__(self):
        checkbox = customtkinter.CTkCheckBox(self.frame, text=self.texto)
        return checkbox

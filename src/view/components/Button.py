import customtkinter

class CustomButton:
    def __init__(self, frame, texto, command=None):
        self.frame = frame
        self.texto = texto
        self.command = command

    def __call__(self):
        button = customtkinter.CTkButton(self.frame, text=self.texto, command=self.command)
        return button

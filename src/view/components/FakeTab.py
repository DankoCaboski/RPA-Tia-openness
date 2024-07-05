from CustomTkinter import customtkinter

class FakeTab:
    def __init__(self, frame, texto=None, command=None):
        self.frame = frame
        self.texto = texto
        self.command = command

    def get_button(self) -> customtkinter.CTkButton:
        button = customtkinter.CTkButton(
            self.frame,
            text=self.texto,
            command=self.command,
            fg_color="transparent",
            bg_color="transparent",
            font=('Helvetica', 12),
            width=60
            )
        
        return button

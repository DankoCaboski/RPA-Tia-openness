from CustomTkinter import customtkinter

import tkinter as tk

class CustomButton:
    def __init__(self, frame, texto=None, image=None, command=None):
        self.frame = frame
        self.texto = texto
        self.image = image
        self.command = command

    def get_button(self) -> customtkinter.CTkButton:
        if self.image is not None:
            button = customtkinter.CTkButton(self.frame, image=self.image, text="", width=24, height=24, command=self.command)
        elif self.texto is not None:
            button = customtkinter.CTkButton(self.frame, text=self.texto, height=24, command=self.command)
        else:
            raise ValueError("Both 'texto' and 'image' cannot be None.")
        
        return button

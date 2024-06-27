from CustomTkinter import customtkinter

from view.components.FakeTab import FakeTab


class TabviewSoftware:
    def __init__(self, frame):
        self.frame  = customtkinter.CTkFrame(frame, fg_color="transparent")
        
        self.frame.pack(fill='both', expand=True)
        
        self.sw_options()
        
    def sw_options(self):
        options_frame = customtkinter.CTkFrame(self.frame, fg_color="#4A4A4A")
        options_frame.grid(row=0, column=0, padx=10, pady=10)
        
        option1 = FakeTab(options_frame, "Robôs")
        option1 = option1.get_button()
        option1.grid(row=0, column=0, padx=10, pady=10)
        
        option2 = FakeTab(options_frame, "Mesa")
        option2 = option2.get_button()
        option2.grid(row=1, column=0, padx=10, pady=10)
        
        option3 = FakeTab(options_frame, "Grampos")
        option3 = option3.get_button()
        option3.grid(row=2, column=0, padx=10, pady=10)
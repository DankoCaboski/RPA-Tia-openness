from CustomTkinter import customtkinter
from view.components.FakeTab import FakeTab


class TabviewSoftware:
    def __init__(self, sw_frame):
        
        frame1 = customtkinter.CTkFrame(sw_frame)
        label1 = customtkinter.CTkLabel(frame1, text="rb")
        label1.pack()
        
        frame2 = customtkinter.CTkFrame(sw_frame)
        label2 = customtkinter.CTkLabel(frame2, text="ms")
        label2.pack()
        
        frame3 = customtkinter.CTkFrame(sw_frame)
        label3 = customtkinter.CTkLabel(frame3, text="gp")
        label3.pack()
    
        
        self.frames = [frame1, frame2, frame3]
        self.current_frame = 0
        
    def sw_content(self, index):
        if index == None:
            return self.frames[self.current_frame]
        else:
            return self.frames[index]
import customtkinter

from view.pages.FrameManagement import FrameManagement

class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("900x1780")
        self.minsize(600,580)
        self.iconbitmap("view/assets/favico.ico")
        
        frame = FrameManagement(self)

app = App()
app.mainloop()
import customtkinter

from view.functions.FrameManagement import FrameManagement

class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("900x1780")
        self.minsize(600,580)
        self.iconbitmap("view/assets/favico.ico")
            
        

app = App()
frame = FrameManagement(app)
app.mainloop()
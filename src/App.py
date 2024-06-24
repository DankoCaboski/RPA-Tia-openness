import customtkinter

from view.functions.FrameManagement import FrameManagement
from openness.controllers.OpennessController import OpennessController
from openness.repositories.DbManagement import DbManagement

class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("900x1780")
        self.minsize(600,580)
        self.iconbitmap("view/assets/favico.ico")

app = App()
database = DbManagement()
database.validate_db()
frame = FrameManagement(app, database)
app.mainloop()
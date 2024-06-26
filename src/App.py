from CustomTkinter import customtkinter
import os


from view.functions.FrameManagement import FrameManagement
from openness.repositories.DbManagement import DbManagement

class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        
        favico_path = ".view/assets/favico.ico"
        if not os.path.exists(favico_path):
            favico_path = "favico.ico"

        self.geometry("720x540")
        self.minsize(600,580)
        self.iconbitmap(favico_path)

app = App()
database = DbManagement()
database.validate_db()
frame = FrameManagement(app, database)
app.mainloop()
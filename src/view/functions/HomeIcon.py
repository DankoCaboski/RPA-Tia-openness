from CustomTkinter import customtkinter
import os

from PIL import Image

class HomeIcon:
    def load_image(self):
        
        home_ico_path = "view/assets/homeIcoDark.png"
        if not os.path.exists(home_ico_path):
            home_ico_path = "homeIcoDark.png"
        
        image = customtkinter.CTkImage(light_image=Image.open(home_ico_path),
                                  dark_image=Image.open(home_ico_path),
                                  size=(15, 15))
        
        return image

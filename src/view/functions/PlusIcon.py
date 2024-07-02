from CustomTkinter import customtkinter
import os

from PIL import Image

class PlusIcon:
    def load_image(self):
        
        home_ico_path = "view/assets/Plus.png"
        if not os.path.exists(home_ico_path):
            home_ico_path = "Plus.png"
        
        image = customtkinter.CTkImage(light_image=Image.open(home_ico_path),
                                  dark_image=Image.open(home_ico_path),
                                  size=(18, 18))
        
        return image

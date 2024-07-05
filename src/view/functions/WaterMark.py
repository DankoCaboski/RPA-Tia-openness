from CustomTkinter import customtkinter

from view.functions.HomeIcon import HomeIcon

import os

from PIL import Image

class WaterMark:
    def load_image(self):
        
        water_mark_path = "view/assets/axix-solution-logo.png"
        if not os.path.exists(water_mark_path):
            water_mark_path = "axix-solution-logo.png"
        
        image = customtkinter.CTkImage(light_image=Image.open(water_mark_path),
                                  dark_image=Image.open(water_mark_path),
                                  size=(377, 90))
        
        return image

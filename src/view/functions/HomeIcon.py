import customtkinter
from PIL import Image

class HomeIcon:
    def load_image(self):
        
        image = customtkinter.CTkImage(light_image=Image.open("view/assets/homeIcoDark.png"),
                                  dark_image=Image.open("view/assets/homeIcoDark.png"),
                                  size=(18, 18))
        
        return image

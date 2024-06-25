import customtkinter
from PIL import Image

class HomeIcon:
    def load_image(self):
        
        image = customtkinter.CTkImage(light_image=Image.open("view/assets/home.png"),
                                  dark_image=Image.open("view/assets/home.png"),
                                  size=(18, 18))
        
        return image

class ButtonHandler:
    def __init__(self, frame_management):
        self.frame_management = frame_management

    def create_project(self):
        self.frame_management.show_create_project_page()
        
    def home_page(self):
        self.frame_management.show_home_page()
        
    def open_project(self):
        self.frame_management.show_open_project_page()

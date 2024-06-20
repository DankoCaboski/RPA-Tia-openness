from view.pages.CreateProject import CreateProject

class ButtonHandler:
    def button_callback(self):
        print("button pressed")
        
    def create_project(self, parent):
        create_project = CreateProject(parent)
        if create_project:
            print("Tela de criar projeto aberta")
            return create_project()
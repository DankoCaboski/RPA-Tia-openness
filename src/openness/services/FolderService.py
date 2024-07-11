class FolderService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        self.sis_gp = None
        self.std_gp = None
        self.op_gp = None
        self.safety_gp = None
        
        self.tt_gp = None
        self.dt_gp = None
        self.cv_gp = None
        self.rb_gp = None
    
    def create_folder_structure(self):
        try:   
            self.create_sistema_structure()
            self.create_std_structure()
            self.create_op_structure()
            self.create_safety_structure()
                    
        except Exception as e:
            print("Error creating operational structure: ", e)
            
        
    def create_sistema_structure(self):
        try:
             if self.sis_gp is None:
                sis_gp = self.tia_service.recursive_group_search(None, "01_Sistema")
                if not sis_gp:
                    self.sis_gp = self.tia_service.create_group(None, "01_Sistema", None)
                    
        except Exception as e:
            print("Error creating operational structure: ", e)
            
        
    def create_std_structure(self):
        try:
             if self.std_gp is None:
                std_gp = self.tia_service.recursive_group_search(None, "02_Blocos Standard Axis")
                if not std_gp:
                    self.std_gp = self.tia_service.create_group(None, "02_Blocos Standard Axis", None)
                    
        except Exception as e:
            print("Error creating operational structure: ", e)
            
            
    def create_op_structure(self):
        try:
            
            if self.op_gp is None:
                op_gp = self.tia_service.recursive_group_search(None, "03_Blocos Operacionais")
                if not op_gp:
                    self.op_gp = self.tia_service.create_group(None, "03_Blocos Operacionais", None)
                    
                    self.create_turntable_structure()
                    self.create_datadores_structure()
                    self.create_conveyor_structure()
                    self.create_robot_structure()
                    
        except Exception as e:
            print("Error creating operational folder structure: ", e)  
            
            
    def create_safety_structure(self):
        try:
             if self.safety_gp is None:
                safety_gp = self.tia_service.recursive_group_search(None, "04_Safety")
                if not safety_gp:
                    self.safety_gp = self.tia_service.create_group(None, "04_Safety", None)
                    
        except Exception as e:
            print("Error creating operational structure: ", e)      
     
            
    def create_turntable_structure(self):
        try:
            self.create_folder_structure()
            
            if self.tt_gp is None:
                tt_gp = self.tia_service.recursive_group_search(None, "03.1_Mesas Giratórias")
                if not tt_gp:
                    self.tt_gp = self.tia_service.create_group(None, "03.1_Mesas Giratórias", "03_Blocos Operacionais")
                    
        except Exception as e:
            print("Error creating operational structure: ", e)
            
            
    def create_datadores_structure(self):
        try:
            self.create_folder_structure()
            
            if self.dt_gp is None:
                dt_gp = self.tia_service.recursive_group_search(None, "03.2_Datadores")
                if not dt_gp:
                    self.dt_gp = self.tia_service.create_group(None, "03.2_Datadores", "03_Blocos Operacionais")
                    
        except Exception as e:
            print("Error creating operational structure: ", e)

            
    def create_conveyor_structure(self):
        try:
            self.create_folder_structure()
            
            if self.cv_gp is None:
                cv_gp = self.tia_service.recursive_group_search(None, "03.3_Esteiras")
                if not cv_gp:
                    self.cv_gp = self.tia_service.create_group(None, "03.3_Esteiras", "03_Blocos Operacionais")
                    
        except Exception as e:
            print("Error creating operational structure: ", e)
            
            
    def create_robot_structure(self):
        try:
            self.create_folder_structure()
            
            if self.rb_gp is None:
                rb_gp = self.tia_service.recursive_group_search(None, "03.4_Robos")
                if not rb_gp:
                    self.rb_gp = self.tia_service.create_group(None, "03.4_Robos", "03_Blocos Operacionais")
                    
        except Exception as e:
            print("Error creating operational structure: ", e)
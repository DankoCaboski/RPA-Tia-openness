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
        
        self.plc_gp = None
        self.celula_gp = None
        self.prodiag_gp = None
        
        self.fb_2005_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2005_FB Robô ABB.xml"
        
        self.raw_ob_list = [1, 121]
    
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
                    
                    self.create_plc_folder()
                    self.create_celula_folder()
                    self.create_prodiag_folder()
                    
        except Exception as e:
            print("Error creating operational structure: ", e)
            
        
    def create_std_structure(self):
        try:
            if self.std_gp is None:
                std_gp = self.tia_service.recursive_group_search(None, "02_Blocos Standard Axis")
                if not std_gp:
                    self.std_gp = self.tia_service.create_group(None, "02_Blocos Standard Axis", None)
                    
            self.tia_service.import_block(self.std_gp.Blocks, self.fb_2005_path)
            
        except Exception as e:
            print("Error creating operational structure: ", e)
            
            
    def create_op_structure(self):
        try:
            
            if self.op_gp is None:
                op_gp = self.tia_service.recursive_group_search(None, "03_Blocos Operacionais")
                if not op_gp:
                    self.op_gp = self.tia_service.create_group(None, "03_Blocos Operacionais", None)
                    
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
     
            
    def create_turntable_structure(self, parent_zone: str, n_zona: int):
        try:
            ms_name = f"z{n_zona}_Mesas Giratórias"
            self.tt_gp = self.tia_service.create_group(None, ms_name, parent_zone)
                    
        except Exception as e:
            print(f"Error creating turntable folder for zone {parent_zone}: ", e)
            
            
    def create_datadores_structure(self):
        try:
            self.create_folder_structure()
            
            if self.dt_gp is None:
                dt_gp = self.tia_service.recursive_group_search(None, "03.2_Datadores")
                if not dt_gp:
                    self.dt_gp = self.tia_service.create_group(None, "03.2_Datadores", "03_Blocos Operacionais")
                    
        except Exception as e:
            print("Error creating operational structure: ", e)

            
    def create_conveyor_structure(self, parent_zone: str, n_zona: int):
        try:
            con_name = f"z{n_zona}_Esteiras"
            self.cv_gp = self.tia_service.create_group(None, con_name, parent_zone)
                    
        except Exception as e:
            print(f"Error creating conveyor folder for zone {parent_zone}: ", e)
            
            
    def create_robot_structure(self, parent_zone: str, n_zona: int):
        try:
            rbz_name = f"z{n_zona}_Robos"
            self.rb_gp = self.tia_service.create_group(None, rbz_name, parent_zone)
            return rbz_name
                    
        except Exception as e:
            print(f"Error creating robot folder for zone {parent_zone}: ", e)
            
        
    def create_plc_folder(self):
        try:
            if self.plc_gp is None:
                plc_gp = self.tia_service.recursive_group_search(None, "01.1_PLC")
                if not plc_gp:
                    self.plc_gp = self.tia_service.create_group(None, "01.1_PLC", "01_Sistema")
                    
            self.move_raw_obs()
                
        except Exception as e:
            print("Error creating plc folder: ", e)
            
        
    def create_celula_folder(self):
        try:
            if self.celula_gp is None:
                celula_gp = self.tia_service.recursive_group_search(None, "01.2_Célula")
                if not celula_gp:
                    self.celula_gp = self.tia_service.create_group(None, "01.2_Célula", "01_Sistema")
                
        except Exception as e:
            print("Error creating celula folder: ", e)
            
    
    def create_prodiag_folder(self):
        try:
            if self.prodiag_gp is None:
                prodiag_gp = self.tia_service.recursive_group_search(None, "01.3_Prodiag")
                if not prodiag_gp:
                    self.prodiag_gp = self.tia_service.create_group(None, "01.3_Prodiag", "01_Sistema")
                
        except Exception as e:
            print("Error creating prodiag folder: ", e)
            
    
    def create_zona_folder(self, n_zona: int):
        try:
            zona_name = f"Zona {n_zona}"
            self.tia_service.create_group(None, zona_name, "03_Blocos Operacionais")
            return zona_name
                
        except Exception as e:
            print("Error creating zona folder: ", e)  
                  
                  
    def move_raw_obs(self):
        try:
            cpu = self.tia_service.cpus[0]
            plc_software = self.tia_service.hwf.get_software(cpu)
            for ob in self.raw_ob_list:
                print(f"Moving OB {ob}")
                
                if ob == 1:
                    plc_software.BlockGroup.Blocks[0].Delete()
                    
                    block_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Raw_OBs\OB01.xml"
                    
                    self.tia_service.import_block(self.plc_gp.Blocks,  block_path)
                
                elif ob == 121:
                    
                    block_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Raw_OBs\OB121.xml"
                    
                    self.tia_service.import_block(self.plc_gp.Blocks,  block_path) 
            
        except Exception as e:
            print("Error moving OB: ", e)
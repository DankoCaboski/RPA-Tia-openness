import customtkinter

class HwFrame:
    def __init__(self, frame):
        self.frame = customtkinter.CTkFrame(frame)
        self.row_counter = 1
        self.add_hw()
    
    def add_hw(self):
        btn_add_hw = customtkinter.CTkButton(self.frame, text="Adicionar Hardware", command=self.add_hw_combobox)
        btn_add_hw.grid(row=0, column=1, columnspan=2, padx=10, pady=10)
        
    def add_hw_combobox(self):
        type_hw = customtkinter.CTkComboBox(self.frame, values=["type1", "type2", "type3"])
        type_hw.grid(row=self.row_counter, column=0, padx=10, pady=10)
        
        hw_mlfb = customtkinter.CTkComboBox(self.frame, values=["mlfb1", "mlfb2", "mlfb3"])
        hw_mlfb.grid(row=self.row_counter, column=1, padx=10, pady=10)
        
        hw_firmware = customtkinter.CTkComboBox(self.frame, values=["firmware1", "firmware2", "firmware3"])
        hw_firmware.grid(row=self.row_counter, column=2, padx=10, pady=10)
        
        hw_name = customtkinter.CTkEntry(self.frame)
        hw_name.grid(row=self.row_counter, column=3, padx=10, pady=10)
        
        self.row_counter += 1
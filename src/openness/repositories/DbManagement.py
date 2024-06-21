import sqlite3
import csv
import os

class DbManagement:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
        file_dir = os.path.dirname(os.path.abspath(__file__))
        openness_dir = os.path.dirname(file_dir)
        self.database_dir = os.path.join(openness_dir, 'database')
    
    def saveDll(self, Tia_Version, dll_Path):
        try:
            self.cursor.execute("INSERT INTO Dll_Path (Tia_Version, Path) VALUES (?, ?)", (Tia_Version, dll_Path))
            self.connection.commit()
            print("DLL path saved successfully.")
            return True
        except sqlite3.IntegrityError:
            print("Error: A DLL path for TIA version {} already exists in the database.".format(Tia_Version))
            return False
        except sqlite3.Error as e:
            print("An error occurred while executing the SQL query:", e)
            return False
        except Exception as e:
            print("An unexpected error occurred:", e)
            return False
            
            
    def getDllPath(self, Tia_Version):
        
        try:
            self.cursor.execute('SELECT path FROM Dll_Path WHERE Tia_Version = ?', (Tia_Version,))
            result = self.cursor.fetchone()
            self.cursor.close()
            return result
        except sqlite3.Error as e:
            print("An error occurred while executing the SQL query:", e)
            return None
            

    def CheckDll(self, Tia_Version):
        if self.getDllPath(Tia_Version):
            return True
        else:
            return False
        
    def create_db(self):
        db_path = os.path.join(self.database_dir, 'Openness.db')
        dll_path = os.path.join(self.database_dir, 'sql', 'ddl.sql')
        
        if not os.path.exists(db_path):
            self.conexao = sqlite3.connect(db_path)
            self.cursor = self.conexao.cursor()
            
            # Carrega o script SQL e executa
            with open(dll_path, 'r') as arquivo_sql:
                script = arquivo_sql.read()
                self.cursor.executescript(script)
            self.conexao.commit()
            
            self.insert_cpu(self.conexao)
            self.insert_ihm(self.conexao)
            self.insert_dll(self.conexao)
            self.conexao.close()
            
    def insert_cpu(self, conexao):
        plc_List_path = os.path.join(self.database_dir, "mlfb", "PLC_List.csv")
        print("Gravando dados na tabela CPU_List")
        with open(plc_List_path, 'r') as arquivo:
            leitor_csv = csv.reader(arquivo)
            for linha in leitor_csv:
                mlfb, type, descricao = linha
                self.cursor.execute("INSERT INTO CPU_List (mlfb, type, description) VALUES (?, ?, ?)", (mlfb, type, descricao))
        self.conexao.commit()

    def insert_dll(self, conexao):
        print("Gravando dados na tabela Dll_Path")
        
        for versao in range(15, 19):
            if versao == 15:
                path = f"C:\\Program Files\\Siemens\\Automation\\Portal V15_1\\PublicAPI\\V15.1\\Siemens.Engineering.dll"
                self.cursor.execute("INSERT INTO Dll_Path (Tia_Version, Path) VALUES (?, ?)", (151, path))
            else:
                path = f"C:\\Program Files\\Siemens\\Automation\\Portal V{versao}\\PublicAPI\\V{versao}\\Siemens.Engineering.dll"
                self.cursor.execute("INSERT INTO Dll_Path (Tia_Version, Path) VALUES (?, ?)", (versao, path))
        self.conexao.commit()
    
    def insert_ihm(self, conexao):
        hmi_List_path = os.path.join(self.database_dir, "mlfb", "IHM_List.csv")
        print("Gravando dados na tabela IHM_List")
        with open(hmi_List_path, 'r') as arquivo:
            leitor_csv = csv.reader(arquivo)
            for linha in leitor_csv:
                mlfb, type, descricao = linha
                self.cursor.execute("INSERT INTO IHM_List (mlfb, type, description) VALUES (?, ?, ?)", (mlfb, type, descricao))
        self.conexao.commit()

    def validate_db(self):
        print("Validating database")
        db_path = os.path.join(self.database_dir, 'Openness.db')
        
        if not os.path.exists(db_path):
            self.create_db()
            
        else:
            self.cursor.execute("SELECT COUNT(*) FROM CPU_List")
            result = self.cursor.fetchone()
            if result[0] == 0:
                self.create_db()
            self.conexao.close()
        
    def getMlfbByHwType(self, hw_type): 
        self.cursor.execute('SELECT mlfb FROM CPU_List WHERE type = ?', (hw_type,))
        return self.cursor.fetchall()
    
    def getMlfbIHMByHwType(self, hw_type):
        self.cursor.execute('SELECT mlfb FROM IHM_List WHERE type = ?', (hw_type,))
        return self.cursor.fetchall()
    
    def getMlfbIOByHwType(self, hw_type):
        self.cursor.execute('SELECT mlfb FROM IO_List WHERE type = ?', (hw_type,))
        return self.cursor.fetchall()
    
    
    def getMlfbByVersion(self, hw_type):
        # Realiza a união das tabelas IHM_List e CPU_List com a tabela VersoesHardware para obter as versões correspondentes
        query = """
        SELECT VersoesHardware.mlfb, VersoesHardware.versao
        FROM IHM_List
        JOIN VersoesHardware ON IHM_List.mlfb = VersoesHardware.mlfb
        WHERE IHM_List.type = ?
        UNION
        SELECT VersoesHardware.mlfb, VersoesHardware.versao
        FROM CPU_List
        JOIN VersoesHardware ON CPU_List.mlfb = VersoesHardware.mlfb
        WHERE CPU_List.type = ?
        UNION
        SELECT VersoesHardware.mlfb, VersoesHardware.versao
        FROM IO_List
        JOIN VersoesHardware ON IO_List.mlfb = VersoesHardware.mlfb
        WHERE IO_List.type = ?
        """
        # Passa o mesmo tipo de hardware para ambas as partes da união
        self.cursor.execute(query, (hw_type, hw_type, hw_type))
        return self.cursor.fetchall()

import pyodbc
from typing import List, Dict, Any
from src.config.settings import settings

class DatabaseManager:
    def __init__(self, config: Dict):
        self.config = config
        self.conn = None
        self.cursor = None

    def _build_connection_string(self) -> str:
        return (
            f"DRIVER={{{settings.SQL_DRIVER}}};"
            f"SERVER={self.config['server']};"
            f"DATABASE={self.config['database']};"
            f"UID={self.config['username']};"
            f"PWD={self.config['password']};"
            f"TrustServerCertificate=yes;"
        )
        
    def connect(self) -> bool:
        """Estabelece conexão com o SQL Server"""
        try:
            self.conn = pyodbc.connect(self._build_connection_string())
            self.cursor = self.conn.cursor()
            print("Conexão estabelecida com sucesso!")
            return True  # Retorna True se conectado com sucesso
        except Exception as e:
            print(f"Erro ao conectar ao SQL Server: {e}")
            self.conn = None
            self.cursor = None
            return False  # Retorna False se falhar
        
    def get_table_schema(self, table_name: str) -> List[Dict]:
        """Obtém esquema da tabela"""
        print(f"Obtendo esquema da tabela: {table_name}")

        query = f"""
        SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}'
        """
        self.cursor.execute(query)
        columns = self.cursor.fetchall()
        
        schema = []
        for col in columns:
            schema.append({
                'name': col.COLUMN_NAME,
                'type': col.DATA_TYPE,
                'max_length': col.CHARACTER_MAXIMUM_LENGTH
            })
        return schema
    
    def get_multiple_table_schemas(self, table_names: List[str]) -> Dict[str, List[Dict]]:
        """Obtém o esquema de múltiplas tabelas"""
        schemas = {}
        for table_name in table_names:
            schemas[table_name] = self.get_table_schema(table_name)
        return schemas

    def get_foreign_keys(self, table_name: str) -> List[Dict]:
        """Obtém chaves estrangeiras para uma tabela"""
        query = f"""
        SELECT 
            OBJECT_NAME(f.parent_object_id) AS source_table,
            COL_NAME(fc.parent_object_id, fc.parent_column_id) AS source_column,
            OBJECT_NAME(f.referenced_object_id) AS target_table,
            COL_NAME(fc.referenced_object_id, fc.referenced_column_id) AS target_column
        FROM 
            sys.foreign_keys AS f
        INNER JOIN 
            sys.foreign_key_columns AS fc 
        ON 
            f.object_id = fc.constraint_object_id
        WHERE 
            OBJECT_NAME(f.parent_object_id) = '{table_name}'
            OR OBJECT_NAME(f.referenced_object_id) = '{table_name}'
        """
        self.cursor.execute(query)
        return [dict(zip(['source_table', 'source_column', 'target_table', 'target_column'], row)) 
                for row in self.cursor.fetchall()]
        
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Executa consulta SQL"""
        print(f"Executando consulta: {query}")
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            # Converter para lista de dicionários
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            return results
        except Exception as e:
            print(f"Erro ao executar consulta: {e}")
            return []
        
    def close(self):
        """Fecha conexão"""
        self.cursor.close()
        self.conn.close()
        print("Conexão fechada.")
        
    def handle_error(self, error: Exception):
        """Tratamento centralizado de erros"""
        # Implementação personalizada
from typing import List, Dict, Any
from src.llm.ollama_client import OllamaClient
from src.core.database import DatabaseManager
from src.utils.sql_utils import validate_sql, clean_sql_query
#from src.utils.error_handling import handle_db_error
from src.config.settings import settings
# src/core/assistant.py

class SQLAIAssistant:
    def __init__(self, db_config: Dict[str, str], model_name: str = "llama3.2"):
        self.db = DatabaseManager(db_config)
        self.llm = OllamaClient(model_name)
        
    def process_nl_request(self, nl_request: str, table_names: List[str]) -> List[Dict[str, Any]]:
        """Processa solicitação em linguagem natural com múltiplas tabelas e JOINs"""

        print(f"Processando solicitação: {nl_request} nas tabelas: {table_names} com o modelo {self.llm.model_name}")
        try:
            schemas = self.db.get_multiple_table_schemas(table_names)
            # Relacionamentos entre as tabelas
            relationships = []
            for table in table_names:
                relationships.extend(self.db.get_foreign_keys(table))
            #print(f"Esquemas das tabelas: {schemas}")
            print(f"Relacionamentos: {relationships}")

            # Se não encontrou relacionamentos, solicitar ao usuário
            if not relationships:
                print("Não foram encontrados relacionamentos entre as tabelas.")
                user_input = input(
                    "Por favor, indique as colunas relacionais no formato 'tabela1.coluna1 = tabela2.coluna2' (separadas por vírgula se houver mais de uma):\n"
                )
                # Exemplo de entrada: "Producao.id_lote = Lotes.id, Produtos.id = Producao.id_produto"
                for rel in user_input.split(","):
                    rel = rel.strip()
                    if "=" in rel:
                        left, right = rel.split("=")
                        left_table, left_col = [x.strip() for x in left.split(".")]
                        right_table, right_col = [x.strip() for x in right.split(".")]
                        relationships.append({
                            "source_table": left_table,
                            "source_column": left_col,
                            "target_table": right_table,
                            "target_column": right_col
                        })
                print(f"Relacionamentos informados pelo usuário: {relationships}")

            sql_query = self.llm.generate_sql_multi_table(nl_request, schemas, relationships)
           
            if not validate_sql(sql_query):
                raise ValueError("Consulta SQL inválida ou insegura")
                
            return self.db.execute_query(sql_query)
            
        except Exception as e:
            print(f"Erro ao processar solicitação: {e}")
            return []



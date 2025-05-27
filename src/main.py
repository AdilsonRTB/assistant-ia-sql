from src.core.assistant import SQLAIAssistant
from src.config.settings import settings
import os
import sys
from src.config.config_env import env_manager

def get_environment_config(env_name: str) -> dict:
    """
    Retorna a configuração específica para cada ambiente
    
    Args:
        env_name: Nome do ambiente (prod, dev, local, staging)
        
    Returns:
        Dicionário com:
        - table_names: Lista de tabelas
        - default_question: Pergunta padrão
        - description: Descrição do ambiente
    """
    env_configs = {
        "prod": {
            "description": "Ambiente de produção detectado. Usando tabelas reais.",
            "table_names": ["Producao", "Produtos", "Lotes", "Consumos"],
            "default_question": "Qual o Lote do produto porca foi usado na producao?"
        },
        "dev": {
            "description": "Ambiente de desenvolvimento detectado. Usando tabelas de exemplo.",
            "table_names": ["st", "se", "sal", "bi"],
            "default_question": "Lista os lotes do artigo com ref MP02.00.001 presente na tabela se indicando a quantidade em stock e armazem na tabela sal?"
        },
        "local": {
            "description": "Ambiente local detectado. Usando tabelas de teste.",
            "table_names": ["Producao", "Produtos", "Lotes", "Consumos"],
            "default_question": "Qual o Lote do produto porca foi usado na producao?"
        },
        "staging": {
            "description": "Ambiente de staging detectado. Usando tabelas de homologação.",
            "table_names": ["Producao", "Produtos", "Lotes", "Consumos"],
            "default_question": "Qual o Lote do produto porca foi usado na producao?"
        }
    }
    
    return env_configs.get(env_name, {
        "description": f"Ambiente '{env_name}' desconhecido. Usando configuração padrão.",
        "table_names": ["Producao", "Produtos", "Lotes", "Consumos"],
        "default_question": "Qual o Lote do produto porca foi usado na producao?"
    })


def main():

    env_name = os.getenv("APP_ENV", "dev")
    if len(sys.argv) > 1:
        env_name = sys.argv[1]
    env_manager.load_environment(env_name)

    # Obter configuração do ambiente
    env_config = get_environment_config(env_name)
    #table_names = env_config["table_names"]
    description = env_config["description"]

    print(f"Ambiente atual: {description}")
    #print(f"Tabelas: {table_names}")
   
    # Pergunta do usuário
    #question = input("Olá Bemvindo, como posso ajudar?\n")

    # Indicar as tabelas disponíveis
    #tabelas = input("Indique as tabelas (ex: Produto, Lote) separadas por vírgula:\n")
    #table_names = [t.strip() for t in tabelas.split(",") if t.strip()]


    # Configuração do banco de dados
    if not os.getenv("DB_SERVER"):
        print("Variáveis de ambiente do banco de dados não encontradas. Usando valores padrão.")
    db_config = {
        "server": os.getenv("DB_SERVER", "127.0.0.1,1433"),
        "database": os.getenv("DB_NAME", "inovprod"),
        "username": os.getenv("DB_USER", "sa"),
        "password": os.getenv("DB_PASSWORD", "AFM1234rtb")
    }
    
    assistant = SQLAIAssistant(db_config, model_name=os.getenv("LLM_MODEL", "llama3.2"))
    
    if assistant.db.connect():
        try:
            while True:
                question = input("\nDigite sua pergunta (ou 'sair' para encerrar):\n")
                if question.strip().lower() in ["sair", "exit", "quit"]:
                    print("Encerrando assistente.")
                    break

                tabelas = input("Indique as tabelas (ex: Produto, Lote) separadas por vírgula:\n")
                table_names = [t.strip() for t in tabelas.split(",") if t.strip()]
                if not table_names:
                    print("Nenhuma tabela informada. Usando configuração padrão.")
                    table_names = env_config["table_names"]

                results = assistant.process_nl_request(
                    question,
                    table_names
                )
                for row in results:
                    print(row)
        finally:
            assistant.db.close()

if __name__ == "__main__":
    main()
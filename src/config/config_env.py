import os
from pathlib import Path
from dotenv import load_dotenv

class EnvironmentManager:
    def __init__(self):
        self.current_env = None
        # Ajuste o caminho para buscar na raiz do projeto
        self.base_dir = Path(__file__).parent.parent.parent  # Volta 3 níveis para a raiz
        
    def load_environment(self, env_name: str = "dev"):
        """Carrega variáveis de ambiente específicas"""
        env_path = self.base_dir / "envs" / f".env.{env_name}"
        
        if not env_path.exists():
            # Lista os arquivos .env disponíveis para ajudar no debug
            env_files = list((self.base_dir / "envs").glob(".env.*"))
            available = [f.suffix[1:] for f in env_files]
            raise FileNotFoundError(
                f"Arquivo .env.{env_name} não encontrado em {env_path}\n"
                f"Arquivos disponíveis: {', '.join(available)}"
            )
            
        load_dotenv(env_path, override=True)
        self.current_env = env_name
        print(f"✓ Ambiente '{env_name}' carregado de {env_path}")
    
    def _clear_environment(self):
        """Limpa variáveis de ambiente carregadas"""
        for key in os.environ.keys():
            if key.startswith(("DB_", "LLM_", "APP_")):
                os.environ.pop(key)
    
    def get_current_environment(self):
        return self.current_env

# Instância global
env_manager = EnvironmentManager()
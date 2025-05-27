import requests
from typing import List, Dict, Any
from src.config.settings import settings
from src.utils.sql_utils import validate_sql, clean_sql_query
from src.llm.prompt_templates import PromptTemplates

class OllamaClient:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.base_url = settings.OLLAMA_URL
        
    def generate_sql_multi_table(self, nl_query: str, schemas: Dict[str, List[Dict]], relationships: List[Dict]) -> str:
        """Gera SQL para múltiplas tabelas"""
        print(f"Gerando SQL multi-tabela para: {nl_query}")
        prompt = PromptTemplates.multi_table_prompt(nl_query, schemas, relationships)
        response = self._call_ollama(prompt)
        return clean_sql_query(response)
        
    def _build_prompt_table(self, nl_query: str, table_name: str, schema: List[Dict]) -> str:
        """Constrói prompt para o LLM"""
        print(f"Construindo prompt para o modelo {self.model_name}")

        return PromptTemplates.basic_sql_generation(
            nl_query=nl_query,
            table_name=table_name,
            schema=schema
        )

        # Usar templates de src/llm/prompt_templates.py
        
    def _call_ollama(self, prompt: str) -> str:
        """Chama API do Ollama"""
        print(f"Chamando API do Ollama com o modelo {self.model_name}")
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.3}
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            print(f"Erro ao chamar Ollama: {e}")
            return ""
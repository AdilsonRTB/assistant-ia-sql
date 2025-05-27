from typing import Optional
import re
from src.config.settings import settings  # Importa configurações

def clean_sql_query(sql_query: str) -> str:
    """Limpa a consulta SQL gerada"""
    if "```sql" in sql_query:
        sql_query = sql_query.split("```sql")[1].split("```")[0]
    elif "```" in sql_query:
        sql_query = sql_query.split("```")[1].split("```")[0]
    return sql_query.strip()

def validate_sql(query: str) -> bool:
    """Validação básica de segurança para consultas SQL"""
    forbidden_keywords = ["DROP", "DELETE", "TRUNCATE", "UPDATE", "INSERT", "ALTER", "CREATE", "EXEC"]
    query_upper = query.upper()
    
    # Permitir apenas SELECT para este exemplo
    if not query_upper.startswith("SELECT"):
        return False
        
    for keyword in forbidden_keywords:
        if keyword in query_upper:
            return False
            
    return True

def extract_tables_from_query(query: str) -> list[str]:
    """
    Extrai os nomes das tabelas mencionadas em uma consulta SQL
    
    Args:
        query: Consulta SQL
        
    Returns:
        Lista de nomes de tabelas encontrados
    """
    # Implementação simplificada - pode ser aprimorada
    tables = re.findall(r'FROM\s+([\w]+)', query, re.IGNORECASE)
    tables += re.findall(r'JOIN\s+([\w]+)', query, re.IGNORECASE)
    return list(set(tables))  # Remove duplicados

def format_sql(query: str) -> str:
    """
    Formata a consulta SQL para melhor legibilidade
    
    Args:
        query: Consulta SQL crua
        
    Returns:
        Consulta formatada com indentação consistente
    """
    # Implementação básica - considerar usar uma lib como sqlparse
    query = re.sub(r'(?i)SELECT', '\nSELECT', query)
    query = re.sub(r'(?i)FROM', '\nFROM', query)
    query = re.sub(r'(?i)WHERE', '\nWHERE', query)
    query = re.sub(r'(?i)GROUP BY', '\nGROUP BY', query)
    query = re.sub(r'(?i)ORDER BY', '\nORDER BY', query)
    return query
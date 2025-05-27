import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
    SQL_DRIVER = "ODBC Driver 18 for SQL Server"
    FORBIDDEN_SQL_KEYWORDS = ["DROP", "DELETE", "TRUNCATE", "UPDATE", "INSERT", "ALTER", "CREATE", "EXEC"]

settings = Settings()
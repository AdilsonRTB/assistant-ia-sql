# IA-LLM SQL Assistant

Este projeto é um assistente inteligente que converte perguntas em linguagem natural (português) em consultas SQL para múltiplas tabelas, utilizando modelos de linguagem (LLM) e integração com banco de dados SQL Server.

## Funcionalidades

- Recebe perguntas do usuário em linguagem natural.
- Permite ao usuário indicar as tabelas envolvidas na consulta.
- Detecta automaticamente relacionamentos entre tabelas (chaves estrangeiras).
- Caso não encontre relacionamentos, solicita ao usuário que informe manualmente as colunas relacionais.
- Gera consultas SQL otimizadas usando LLM (ex: Ollama).
- Executa a consulta no banco de dados e retorna os resultados.
- Suporte a múltiplos ambientes (dev, prod, staging, local) via variáveis de ambiente.

## Como usar

1. **Configuração de ambiente:**  
   Defina as variáveis de ambiente ou utilize arquivos `.env` para cada ambiente em `/envs/.env.<ambiente>`.

2. **Executando o assistente:**
   ```bash
   # Defina o ambiente (opcional, padrão: dev)
   set APP_ENV=prod
   python src/main.py
   ```
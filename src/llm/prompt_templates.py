from typing import List, Dict

class PromptTemplates:
    @staticmethod
    def basic_sql_generation(nl_query: str, table_name: str, schema: List[Dict]) -> str:
        """
        Template básico para geração de SQL a partir de linguagem natural
        
        Args:
            nl_query: Consulta em linguagem natural
            table_name: Nome da tabela alvo
            schema: Esquema da tabela (nome, tipo, max_length)
            
        Returns:
            Prompt formatado para o LLM
        """
        schema_str = "\n".join([f"- {col['name']} ({col['type']})" for col in schema])
        
        return f"""
        Você é um especialista em SQL Server. Converta a seguinte solicitação em linguagem natural
        para uma consulta SQL válida usando APENAS a tabela '{table_name}' com o seguinte esquema:

        ### Esquema da tabela {table_name}:
        {schema_str}

        ### Solicitação:
        {nl_query}

        ### Regras importantes:
        1. Retorne APENAS o código SQL, sem explicações ou comentários
        2. Use apenas o esquema fornecido - NÃO INVENTE COLUNAS
        3. Verifique cuidadosamente os nomes das colunas
        4. Para agregações, use GROUP BY quando necessário
        5. Mantenha a consulta eficiente e bem formatada

        ### SQL:
        """

    @staticmethod
    def advanced_sql_generation(nl_query: str, table_name: str, schema: List[Dict], examples: List[Dict] = None) -> str:
        """
        Template avançado com exemplos para few-shot learning
        
        Args:
            nl_query: Consulta em linguagem natural
            table_name: Nome da tabela alvo
            schema: Esquema da tabela
            examples: Exemplos de NL->SQL (opcional)
            
        Returns:
            Prompt formatado para o LLM
        """
        schema_str = "\n".join([f"- {col['name']} ({col['type']})" for col in schema])
        
        examples_section = ""
        if examples:
            examples_section = "\n### Exemplos:\n" + "\n\n".join(
                [f"NL: {ex['nl']}\nSQL: {ex['sql']}" for ex in examples]
            )
        
        return f"""
        Você é um especialista em SQL Server com 15 anos de experiência. Sua tarefa é converter
        solicitações em linguagem natural para consultas SQL otimizadas usando APENAS a tabela '{table_name}'.

        ### Esquema completo:
        {schema_str}
        {examples_section}

        ### Solicitação atual:
        {nl_query}

        ### Diretrizes:
        1. Retorne SOMENTE o código SQL sem comentários
        2. Priorize consultas eficientes (usar índices quando possível)
        3. Use JOINs apenas se necessário
        4. Formate o SQL para legibilidade
        5. Trate valores nulos adequadamente

        ### SQL:
        """

    @staticmethod
    def schema_aware_prompt(nl_query: str, table_name: str, schema: List[Dict]) -> str:
        """
        Template com foco em conscientização do esquema para evitar erros comuns
        
        Args:
            nl_query: Consulta em linguagem natural
            table_name: Nome da tabela alvo
            schema: Esquema da tabela
            
        Returns:
            Prompt altamente estruturado
        """
        columns_str = "\n".join([f"{col['name']} ({col['type']})" for col in schema])
        
        return f"""
        # Tarefa: Conversão NL para SQL
        ## Contexto:
        - Banco de dados: SQL Server
        - Tabela: {table_name}
        - Colunas disponíveis:
        {columns_str}

        ## Solicitação do usuário:
        "{nl_query}"

        ## Instruções:
        1. Analise cuidadosamente o esquema antes de gerar o SQL
        2. Considere os tipos de dados das colunas
        3. Verifique se todos os campos referenciados existem
        4. Retorne APENAS o SQL, sem marcações ou explicações

        ## Restrições:
        - Proibido usar: DROP, DELETE, TRUNCATE, UPDATE, INSERT, ALTER, CREATE, EXEC
        - Somente consultas SELECT
        - Não invente colunas que não existem

        ## SQL Resultante:
        """

    @staticmethod
    def error_correction_prompt(bad_sql: str, error_msg: str, table_name: str, schema: List[Dict]) -> str:
        """
        Template para correção de SQL com base em erros de execução
        
        Args:
            bad_sql: Consulta SQL com erro
            error_msg: Mensagem de erro do banco de dados
            table_name: Nome da tabela
            schema: Esquema da tabela
            
        Returns:
            Prompt para correção de SQL
        """
        schema_str = "\n".join([f"- {col['name']} ({col['type']})" for col in schema])
        
        return f"""
        A seguinte consulta SQL falhou com o erro: {error_msg}
        
        Consulta com erro:
        {bad_sql}

        Esquema da tabela {table_name}:
        {schema_str}

        Por favor, corrija a consulta SQL seguindo estas regras:
        1. Mantenha a intenção original da consulta
        2. Corrija apenas o necessário para resolver o erro
        3. Verifique especialmente:
           - Nomes de colunas
           - Tipos de dados
           - Sintaxe SQL
        4. Retorne APENAS a consulta corrigida, sem explicações

        Consulta corrigida:
        """
    
    @staticmethod
    def multi_table_prompt(nl_query: str, schemas: Dict[str, List[Dict]], relationships: List[Dict]) -> str:
        """
        Template para consultas envolvendo múltiplas tabelas
        
        Args:
            nl_query: Consulta em linguagem natural
            schemas: Dicionário com esquemas de todas as tabelas relevantes
            relationships: Lista de relacionamentos entre tabelas
            
        Returns:
            Prompt formatado para o LLM
        """
        schema_sections = []
        for table_name, columns in schemas.items():
            cols = "\n".join([f"- {col['name']} ({col['type']})" for col in columns])
            schema_sections.append(f"### Tabela {table_name}:\n{cols}")
        
        rel_section = ""
        if relationships:
            rels = "\n".join([f"{rel['source_table']}.{rel['source_column']} → {rel['target_table']}.{rel['target_column']}" 
                            for rel in relationships])
            rel_section = f"\n### Relacionamentos:\n{rels}"
        
        return f"""
        Você é um especialista em SQL Server. Converta a solicitação abaixo em uma consulta SQL válida
        usando as seguintes tabelas e seus relacionamentos:

        {''.join(schema_sections)}
        {rel_section}

        ### Solicitação:
        {nl_query}

        ### Regras:
        1. Use JOINs apropriados baseados nos relacionamentos fornecidos
        2. Inclua apenas as colunas necessárias
        3. Use aliases de tabela para evitar ambiguidade
        4. Retorne APENAS o SQL, sem explicações
        5. Use apenas o esquema fornecido - NÃO INVENTE COLUNAS
        6. Verifique cuidadosamente os nomes das colunas
        7. Para agregações, use GROUP BY quando necessário
        58 Mantenha a consulta eficiente e bem formatada

        ### SQL:
        """

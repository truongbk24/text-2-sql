from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agent.DatabaseManager import DatabaseManager
from agent.LLMManager import LLMManager
from agent.State import InputState, OutputState
from dotenv import load_dotenv
import os
load_dotenv()

class SQLAgent:
    def __init__(self, schema_name: str = "sample"):
        self.db_manager = DatabaseManager(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 5432)),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password"),
            database=os.getenv("DB_NAME", "text2sql"))
#     )
        self.llm_manager = LLMManager(api_key=os.getenv("GOOGLE_API_KEY",""),model="gemini-2.5-flash")        
        self.schema_name = schema_name
        
    def parsed_question(self, state: OutputState) -> dict:
        question = state["question"]
        schema = self.db_manager.get_schema(self.schema_name)
        prompt = ChatPromptTemplate.from_messages([
            ('system', '''
                You are a helpful assistant that translates natural language questions into SQL queries, parse user questions about a database.
                Given the question and database schema, identify the relevant tables and columns.
                If the question is not relevant to the database or if there is not enough information to answer the question, set is_relevant to false.
                
                Your response should be in the following JSON format:
                {{
                    "is_relevant": boolean,
                    "relevant_tables": [
                        {{
                            "table_name": string,
                            "columns": [string]
                        }}
                    ]
                }}
             '''),
            ("human", """
              ===Database schema: 
              {schema}
              ===User question: 
              {question}
              Identify the relevant tables and columns for the question based on the database schema. 
             """)
        ])
        output_parser = JsonOutputParser()
        response = self.llm_manager.invoke(prompt,schema=schema, question=question)
        parsed_response = output_parser.parse(response)        
        return {"parsed_question": parsed_response}
    
    def generate_sql(self, state: OutputState) -> dict:
        question = state['question']
        parsed_question = state['parsed_question']
        if not parsed_question['is_relevant']:
            return {"sql_query": "NOT RELEVANT", "is_relevant": False}
        schema = self.db_manager.get_schema(self.schema_name)
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
                You are an AI assistant that generates SQL queries based on user questions, database schema, and unique nouns found in the relevant tables. Generate a valid SQL query to answer the user's question.
                If there is not enough information to write a SQL query, respond with "NOT_ENOUGH_INFO".
                SKIP ALL ROWS WHERE ANY COLUMN IS NULL, skip all rows where "N/A" or "" only if the column is string type.
                Just give the query string. Do not format it. 
             """),
            ("human", """
              ===User question: 
              {question}
              ===Relevant tables and columns:
              {parsed_question}
              ===Database schema:
              {schema}
              Generate an SQL query string
             """)
        ])
        response = self.llm_manager.invoke(prompt, schema=schema, parsed_question=parsed_question, question=question)
        if response.strip() == "NOT_ENOUGH_INFO":
            return {"sql_query": "NOT_RELEVANT"}
        else:
            return {"sql_query": response}
        
    def validate_and_fix_sql(self, state: OutputState) -> dict:
        sql_query = state['sql_query']
        if sql_query in ["NOT_RELEVANT"]:
            return {"sql_valid": False, "sql_query": "NOT_RELEVANT"}
        schema = self.db_manager.get_schema(self.schema_name)
        prompt = ChatPromptTemplate.from_messages([
            ("system", '''
            You are an AI assistant that validates and fixes SQL queries. Your task is to:
            1. Check if the SQL query is valid.
            2. Ensure all table and column names are correctly spelled and exist in the schema.
            3. If there are any issues, fix them and provide the corrected SQL query.
            4. If no issues are found, return the original query.

            Respond in JSON format with the following structure. Only respond with the JSON:
            {{
                "valid": boolean,
                "issues": string or null,
                "corrected_query": string
            }}
            '''),
                        ("human", '''===Database schema:
            {schema}

            ===Generated SQL query:
            {sql_query}

            Respond in JSON format with the following structure. Only respond with the JSON:
            {{
                "valid": boolean,
                "issues": string or null,
                "corrected_query": string
            }}

            For example:
            1. {{
                "valid": true,
                "issues": null,
                "corrected_query": "None"
            }}
                        
            2. {{
                "valid": false,
                "issues": "Column USERS does not exist",
                "corrected_query": "SELECT * FROM `users` WHERE age > 25"
            }}
                        
            '''),
                    ])

        output_parser = JsonOutputParser()
        response = self.llm_manager.invoke(prompt, schema=schema, sql_query=sql_query)
        result = output_parser.parse(response)

        if result["valid"] and result["issues"] is None:
            return {"sql_query": sql_query, "sql_valid": True}
        else:
            print(result["corrected_query"])
            return {
                "sql_query": result["corrected_query"],
                "sql_valid": result["valid"],
                "sql_issues": result["issues"]
            }
            
    def execute_sql(self, state: OutputState) -> dict:
        """Execute the SQL query and return results."""
        query = state['sql_query']
        if query in ["NOT_RELEVANT"]:
            return {"results": "NOT_RELEVANT"}
        try:
            results = self.db_manager.execute_query(query)
            return {"results": results}
        except Exception as e:
            return {"results": f"ERROR: {str(e)}"}
        
    def format_results(self, state: OutputState) -> dict:
        """Format the results into a user-friendly answer."""
        question = state['question']
        results = state['results']
        if results in ["NOT_RELEVANT"]:
            return {"answer": "The question is not relevant to the database."}
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI assistant that formats database query results into a human-readable response. Give a conclusion to the user's question based on the query results. Do not give the answer in markdown format. Only give the answer in one line."),
            ("human", "User question: {question}\n\nQuery results: {results}\n\nFormatted response:"),
        ])
        response = self.llm_manager.invoke(prompt, question=question, results=results)
        return {"answer": response}
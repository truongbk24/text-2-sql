# #!/usr/bin/env python3
# """
# Main script to test DatabaseManager functionality.
# """

# import os
# from dotenv import load_dotenv
# from DatabaseManager import DatabaseManager
# from LLMManager import LLMManager
# import google.generativeai as genai
# from langchain_core.prompts import ChatPromptTemplate

# # Load environment variables from .env file
# load_dotenv()


# def test_database_manager():
#     """Test the DatabaseManager class."""
#     print("Testing DatabaseManager...")
    
#     # Initialize DatabaseManager with environment variables
#     db_manager = DatabaseManager(
#         host=os.getenv("DB_HOST", "localhost"),
#         port=int(os.getenv("DB_PORT", 5432)),
#         user=os.getenv("DB_USER", "postgres"),
#         password=os.getenv("DB_PASSWORD", "password"),
#         database=os.getenv("DB_NAME", "text2sql")
#     )
    
#     # Test get_schema
#     try:
#         schema = db_manager.get_schema(schema_name="sample")
#         print("✓ Schema retrieved successfully")
#         print(f"results: {schema}")
#     except Exception as e:
#         print(f"✗ Failed to retrieve schema: {e}")
    
#     # Test execute_query
#     try:
#         results = db_manager.execute_query("SELECT 1 as test_value")
#         print("✓ Query executed successfully")
#         print(f"  Results: {results}")
#     except Exception as e:
#         print(f"✗ Failed to execute query: {e}")


# def test_llm_manager():
#     """Test the LLMManager class."""
#     print("\nTesting LLMManager...")
    
#     # Get Google API key from environment
#     api_key = os.getenv("GOOGLE_API_KEY")
    
#     # genai.configure(api_key=api_key)

#     # for m in genai.list_models():
#     #     print(m.name, m.supported_generation_methods)
    
#     if not api_key:
#         print("⚠ GOOGLE_API_KEY not set in .env file")
#         return
    
#     try:
#         llm_manager = LLMManager(api_key=api_key, model="gemini-2.5-flash")
#         print("✓ LLMManager initialized successfully")
        
#         prompt = ChatPromptTemplate.from_messages([
#             ("human", f"What is the capital of France?")
#         ])
#         # Test invoke
#         response = llm_manager.invoke(prompt)
#         print("✓ LLM invocation successful")
#         print(f"  Response: {response[:100]}...")
#     except Exception as e:
#         print(f"✗ LLMManager test failed: {e}")


# if __name__ == "__main__":
#     print("=" * 50)
#     print("Testing Agent Components")
#     print("=" * 50)
    
#     test_database_manager()
#     test_llm_manager()
    
from agent.WorkflowManager import WorkflowManager

graph = WorkflowManager().returnGraph()

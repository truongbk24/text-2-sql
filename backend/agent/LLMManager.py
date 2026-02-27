from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional


class LLMManager:
    """Manages interactions with Google Gemini models using LangChain for the text-2-sql agent."""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        """
        Initialize the LLM manager with Google Gemini via LangChain.
        
        Args:
            api_key: Google API key
            model: Model name to use (default: gemini-pro)
        """
        self.api_key = api_key
        self.model = model
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key
        )
    
    def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> str:
        """
        Send a prompt to Google Gemini model via LangChain and get a response.
        
        Args:
            prompt: The user prompt/query to send to the model
            system_instruction: Optional system instruction for the model
            
        Returns:
            The model's text response
        """
        try:
            print(f"LLM messages: starting to invoke model with prompt: {prompt} and kwargs: {kwargs}")
            messages = prompt.format_messages(**kwargs) 
            response = self.llm.invoke(messages)
            # Extract text content from response
            return response.content if hasattr(response, 'content') else str(response) # type: ignore
            
        except Exception as e:
            raise Exception(f"Error invoking Google Gemini model via LangChain: {str(e)}")

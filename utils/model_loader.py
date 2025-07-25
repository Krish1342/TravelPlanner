import os
from dotenv import load_dotenv
from typing import Literal, Optional
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

class ConfigLoader:
    def __init__(self):
        print("Loading configuration...")
        self.config = load_config()
        print("Configuration loaded.")

    def __getitem__(self, key):
        return self.config[key]


class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default_factory=ConfigLoader, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        """
        Load and return the LLM model based on the provider.
        """
        print("\nLoading LLM...")
        print(f"Provider selected: {self.model_provider}")

        if self.model_provider == "groq":
            print("Using Groq provider...")
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY is not set in environment variables.")
            try:
                model_name = self.config["llm"]["groq"]["model"]
            except (KeyError, TypeError):
                raise ValueError("Missing 'model' key under 'llm.groq' in config.")
            llm = ChatGroq(model=model_name, api_key=groq_api_key)

        elif self.model_provider == "openai":
            print("Using OpenAI provider...")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY is not set in environment variables.")
            try:
                model_name = self.config["llm"]["openai"]["model"]
            except (KeyError, TypeError):
                raise ValueError("Missing 'model' key under 'llm.openai' in config.")
            llm = ChatOpenAI(model_name=model_name, api_key=openai_api_key)

        else:
            raise ValueError(f"Unknown model provider: {self.model_provider}")

        print(f"✅ Model '{model_name}' loaded successfully.\n")
        return llm

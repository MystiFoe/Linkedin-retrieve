# File: src/config.py
import os
import json
from dotenv import load_dotenv
from .logger import app_logger

class Config:
    """Configuration class for the application"""
    
    @staticmethod
    def load_config():
        """Load environment variables from .env file or Streamlit secrets"""
        # Try to load from .env file for local development
        load_dotenv()
        app_logger.info("Loading environment variables")
        
        # Initialize config with default values
        config = {
            "TEXAU_API_KEY": None,
            "TEXAU_BASE_URL": "https://api.texau.com/api/v1",
            "TEXAU_CONTEXT": None,
            "HF_TOKEN": None  # Added HF_TOKEN
        }
        
        # First try to get from Streamlit secrets if available
        try:
            import streamlit as st
            if hasattr(st, 'secrets'):
                app_logger.info("Trying to load from Streamlit secrets")
                config["TEXAU_API_KEY"] = st.secrets.get("TEXAU_API_KEY")
                config["TEXAU_BASE_URL"] = st.secrets.get("TEXAU_BASE_URL", config["TEXAU_BASE_URL"])
                config["TEXAU_CONTEXT"] = st.secrets.get("TEXAU_CONTEXT")
                config["HF_TOKEN"] = st.secrets.get("HF_TOKEN")
                config["NEWSAPI_KEY"] = st.secrets.get("NEWSAPI_KEY")  # Added NEWSAPI_KEY
        except (ImportError, AttributeError) as e:
            app_logger.info(f"Streamlit secrets not available: {str(e)}")
        
        # If not found in Streamlit secrets, try environment variables
        if not config["TEXAU_API_KEY"]:
            config["TEXAU_API_KEY"] = os.getenv("TEXAU_API_KEY")
        if not config["TEXAU_CONTEXT"]:
            config["TEXAU_CONTEXT"] = os.getenv("TEXAU_CONTEXT")
        if not config["HF_TOKEN"]:
            config["HF_TOKEN"] = os.getenv("HF_TOKEN")  # Added HF_TOKEN
        if os.getenv("TEXAU_BASE_URL"):
            config["TEXAU_BASE_URL"] = os.getenv("TEXAU_BASE_URL")
        
        # Check if required environment variables are set
        if not config["TEXAU_API_KEY"]:
            app_logger.error("TEXAU_API_KEY not found in environment variables or Streamlit secrets")
            raise ValueError("TEXAU_API_KEY not found in environment variables or Streamlit secrets")
        
        if not config["TEXAU_CONTEXT"]:
            app_logger.warning("TEXAU_CONTEXT not found in environment variables or Streamlit secrets")
            
        if not config["HF_TOKEN"]:
            app_logger.warning("HF_TOKEN not found in environment variables or Streamlit secrets")
            
        return config
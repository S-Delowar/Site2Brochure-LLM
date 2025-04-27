import os
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model for link generator and brochure creator
MODEL = "gpt-4o-mini"

from langchain_groq import ChatGroq
import os
import dotenv
dotenv.load_dotenv()
api_key=os.getenv("GROQ_API_KEY")

def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.2,
        max_tokens=1024,
        api_key=api_key
    )

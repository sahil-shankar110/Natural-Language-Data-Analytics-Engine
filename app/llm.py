from langchain_groq import ChatGroq
from app.prompts import sql_prompt
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    api_key= groq_api_key,
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.4,
    max_tokens=None,
    max_retries=2)
    
chain =  sql_prompt| llm | JsonOutputParser() 

def generate_sql(table_name, schema, sample_rows, question):
    """
    Takes user question + table info.
    Returns SQL, explanation, chart info as a dict.
    """

    try:
        result = chain.invoke({
            "table_name": table_name,
            "schema": schema,
            "sample_rows": sample_rows,
            "question": question
        })
        return result

    except Exception:
        raise ValueError("Oops! Something went wrong, please try again.")

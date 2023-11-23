from langchain.llms import Together
from pathlib import Path
from dotenv import load_dotenv
import os

from together_ai.configuration.log_factory import logger

load_dotenv()

class Config:
    llm = Together(
        model= os.getenv("MODEL"),
        temperature= eval(os.getenv("TEMPERATURE")),
        max_tokens= int(os.getenv("MAX_TOKENS")),
        top_k= int(os.getenv("TOP_K")),
        together_api_key= os.getenv("TOGETHER_API_KEY"),
        verbose = True
    )

cfg = Config()

if __name__ == "__main__":
    logger.info(cfg.llm)
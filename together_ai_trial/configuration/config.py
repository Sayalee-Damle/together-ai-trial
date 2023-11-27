from langchain.llms import Together
from pathlib import Path
from dotenv import load_dotenv
import os


from together_ai_trial.configuration.log_factory import logger


load_dotenv()

class Config:

    def select_model(self, model_name_val, temperature_val, max_tokens_val, top_k_val):
            
        llm = Together(
            model = model_name_val,
            temperature= temperature_val,
            max_tokens= max_tokens_val,
            top_k= top_k_val,
            together_api_key= os.getenv("TOGETHER_API_KEY"),
            top_p = 0.7,
            repetition_penalty = 1
        )
        return llm


    project_root = Path(os.getenv("PROJECT_ROOT"))
    assert project_root.exists()

    together_api_key= os.getenv("TOGETHER_API_KEY")

cfg = Config()

if __name__ == "__main__":
    print(cfg.project_root)
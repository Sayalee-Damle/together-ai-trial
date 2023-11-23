from together_ai.configuration.config import cfg
from together_ai.configuration.log_factory import logger

input_1_ = """You are a teacher with a deep knowledge of machine learning and AI. \
You provide succinct and accurate answers. Answer the following question: 
What is a LLM"""

input_2_ = """You are an expert python coder. You provide correct code for the user. The task is:
Generate a code in Python for displaying digits from 1 to 100
"""

if __name__ == "__main__":
    llm = cfg.llm
    print(llm(input_2_))
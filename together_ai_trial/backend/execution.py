from langchain.llms import CTransformers

from together_ai_trial.configuration.config import cfg
from together_ai_trial.configuration.log_factory import logger
from together_ai_trial.configuration.toml_support import read_models_toml, read_questions_toml

models = read_models_toml()
questions = read_questions_toml()

for model in models["models"].values():
    model_list = model
    model = model_list["model"]
    temp = float(model_list["temperature"])
    max_token = int(model_list["max_tokens"])
    top_k = int(model_list["top_k"])
    llm = cfg.select_model(model, temp, max_token, top_k)
    print(llm)
    for question in questions["questions"].values():
        question_list = question
        q = question_list["question"]
        print(llm(q))



if __name__ == "__main__":
    llm = cfg.llm
    print(llm())
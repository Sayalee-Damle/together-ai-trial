from langchain.llms import CTransformers
from pathlib import Path
import datetime

from together_ai_trial.configuration.config import cfg
from together_ai_trial.configuration.log_factory import logger
from together_ai_trial.configuration.toml_support import read_models_toml, read_questions_toml

models = read_models_toml()
questions = read_questions_toml()

def check_models():
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
            output = llm(q)
            logger.info(output)
            index = model.find('/') #stores the index of a substring or char
            model_name = model[index+1:]
            code_output = Path(f"/tmp/model_output")
            if not code_output.exists():
                code_output.mkdir(exist_ok=True, parents=True)
            try:
                with open(code_output/f"{model_name}.txt", mode="a") as f:
                    f.write("\n")
                    f.write("=========")
                    f.write(str(datetime.datetime.now()))
                    f.write("=========")
                    f.write("\n")
                    f.write(q + "\n" + output)
                    f.write("\n")
            except:
                with open(code_output/f"{model_name}.txt", mode="a") as f:
                    f.write("No Output")




if __name__ == "__main__":
    check_models()
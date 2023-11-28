import datetime
from pathlib import Path
import together

from together_ai_trial.configuration.config import cfg
from together_ai_trial.configuration.toml_support import read_questions_toml
from together_ai_trial.backend.models_list import large_models

questions = read_questions_toml()


together.api_key = cfg.together_api_key

model_list = together.Models.list()

print(f"{len(model_list)} models available")

# print the first 10 models on the menu
model_names = [model_dict['name'] for model_dict in model_list]


code_output = Path(f"/tmp/model_output")
if not code_output.exists():
    code_output.mkdir(exist_ok=True, parents=True)
with open(code_output/"model_names.txt", mode="w") as f:
    f.write("\n".join(model_names))

for model_name in model_names:
    if "instruct" in model_name.lower():
        continue
    print(model_name)
    for question in questions["questions"].values():
        question_list = question
        q = question_list["question"]
        try:
            output = together.Complete.create(
                prompt = f"<human>: {q}\n<bot>:", 
                model = model_name, 
                max_tokens = 500,
                temperature = 0.8,
                top_k = 60,
                top_p = 0.6,
                repetition_penalty = 1.1,
                stop = ['<human>', '\n\n']
                )
            print(output["output"])
            index = model_name.find('/') #stores the index of a substring or char
            model_name_file = model_name[index+1:]
            code_output = Path(f"/tmp/model_output")
            if not code_output.exists():
                code_output.mkdir(exist_ok=True, parents=True)

            with open(code_output/f"{model_name_file}.txt", mode="a+") as f:
                f.write("\n")
                f.write("=========")
                f.write(str(datetime.datetime.now()))
                f.write("=========")
                f.write("\n")
                f.write(q + "\n" +output["output"]["choices"][0]["text"])
                f.write("\n")


        except:
            continue
        


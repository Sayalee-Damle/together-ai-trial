import datetime
import pathlib
import time
import together

from together_ai_trial.configuration.toml_support import read_questions_toml
from together_ai_trial.configuration.config import cfg

questions = read_questions_toml()


large_models = [
    "Austism/chronos-hermes-13b",
    "togethercomputer/GPT-NeoXT-Chat-Base-20B",
    "togethercomputer/llama-2-13b-chat",
    "togethercomputer/llama-2-70b-chat",
    "Gryphe/MythoMax-L2-13b",
    "NousResearch/Nous-Hermes-Llama2-13b",
    "NousResearch/Nous-Hermes-Llama2-70b",
    "garage-bAInd/Platypus2-70B-instruct",
    "lmsys/vicuna-13b-v1.5",
    "lmsys/vicuna-13b-v1.5-16k",
    "togethercomputer/CodeLlama-13b",
    "togethercomputer/CodeLlama-34b",
    "togethercomputer/CodeLlama-13b-Python",
    "togethercomputer/CodeLlama-34b-Python"
    "Phind/Phind-CodeLlama-34B-Python-v1",
    "Phind/Phind-CodeLlama-34B-v2",
    "WizardLM/WizardCoder-15B-V1.0"
]

together.api_key = cfg.together_api_key


for model_name in large_models:
    #print(model_name)
    for question in questions["questions"].values():
        question_list = question
        q = question_list["question"]
        try:
            #print("in for")
            time_start = time.perf_counter()
            output = together.Complete.create(
                prompt = f"<human>: {q}\n<bot>:", 
                model =  model_name, 
                max_tokens = 500,
                temperature = 0.1,
                top_k = 50,
                top_p = 0.6,
                repetition_penalty = 1.1,
                stop = ['<human>', '\n\n']
                )
            #print(output["output"]["choices"][0]["text"])
            time_elapsed = (time.perf_counter() - time_start)
            print(time_elapsed)
            index = model_name.find('/') #stores the index of a substring or char
            model_name_file = model_name[index+1:]
            code_output = pathlib.Path(f"/tmp/model_output")
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
                f.write("time required: " + str(time_elapsed))
                f.write("\n")
                f.write("\n")


        except:
            print("in except")
            continue


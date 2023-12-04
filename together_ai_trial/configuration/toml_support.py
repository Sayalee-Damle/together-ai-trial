from pathlib import Path
import time
import together
import tomli

from together_ai_trial.configuration.config import cfg


def read_toml(file: Path) -> dict:
    with open(file, "rb") as f:
        return tomli.load(f)


def read_models_toml() -> dict:
    return read_toml(cfg.project_root / "models.toml")

def read_questions_toml() -> dict:
    return read_toml(cfg.project_root / "questions.toml")

def read_prompts_toml() -> dict:
    return read_toml(cfg.project_root / "prompts.toml")



models = read_models_toml()
questions = read_questions_toml()
prompts = read_prompts_toml()

if __name__ == "__main__":
    for model in models["models"]:
        print(model)
    
    for q in questions["questions"].values():
        print(q["question"])
        together.api_key = cfg.together_api_key
        ques = q["question"]
        time_start = time.perf_counter()
        output = together.Complete.create(
                        prompt = f"<human>: {ques}\n<bot>:", 
                        model = "togethercomputer/CodeLlama-13b-Python", 
                        max_tokens = 256,
                        temperature = 0.8,
                        top_k = 60,
                        top_p = 0.6,
                        repetition_penalty = 1.1,
                        stop = ['<human>', '\n\n']
                        )
        
        print(output["output"]["choices"][0]["text"])
        time_elapsed = (time.perf_counter() - time_start)
        print(time_elapsed)
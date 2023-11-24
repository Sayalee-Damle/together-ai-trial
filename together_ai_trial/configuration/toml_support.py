from pathlib import Path
import tomli

from together_ai_trial.configuration.config import cfg


def read_toml(file: Path) -> dict:
    with open(file, "rb") as f:
        return tomli.load(f)


def read_models_toml() -> dict:
    return read_toml(cfg.project_root / "models.toml")

def read_questions_toml() -> dict:
    return read_toml(cfg.project_root / "questions.toml")



models = read_models_toml()
questions = read_questions_toml()

if __name__ == "__main__":
    for model in models["models"].values():
        print(model)
    
    for q in questions["questions"].values():
        print(q["question"])
    #print(questions)
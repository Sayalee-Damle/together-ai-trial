import datetime
from pathlib import Path

from pylint.lint.run import Run

import together_ai_trial.services.extract_code_service as code_service
from together_ai_trial.configuration.config import cfg


async def lint_code(code, question, model):
    
    d = datetime.datetime.now()
    date_now = d.date()
    question_name = question.replace(" ", "")
    question_name.strip("\n")
    code_output = cfg.code_output
    code_output_module = Path(f"{code_output}/{date_now}_{question_name}")
    if not code_output_module.exists():
        code_output_module.mkdir(exist_ok=True, parents=True)
    index = model.find('/') #stores the index of a substring or char
    model_name = model[index+1:]
    output_file = code_output_module / f"{model_name}_lint.txt"
    code_extract = code_service.extract_code(code)
    temp_file = code_output/"temp.py"
    temp_file.write_text(code_extract, encoding="utf-8")
    Run([f"--output={output_file}", temp_file.as_posix()], exit=False)
    return output_file


if __name__ == "__main__":
    import asyncio

    model = "WizardLM/WizardCoder-15B-V1.0"
    question = "Generate python code to display numbers from 1 to 30"
    code = """"
    ```python
for i in range(1, 31):
    print(i)
```

This code uses a for loop and the `range()` function to iterate over the numbers from 1 to 30 (inclusive) and print each number on a new line. 
The `range()` function generates a sequence of numbers starting from the first argument (1) and ending at the second argument (31), incrementing by 1 each time.
    """
    output_file = asyncio.run(lint_code(code, question, model))
    assert output_file is not None
    assert output_file.exists()
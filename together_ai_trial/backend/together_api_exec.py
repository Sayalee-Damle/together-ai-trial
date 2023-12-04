import datetime
import pathlib
import time
import together
import pandas as pd
from openpyxl import load_workbook
import openpyxl



from together_ai_trial.configuration.config import cfg
from together_ai_trial.configuration.log_factory import logger
from together_ai_trial.configuration.toml_support import read_prompts_toml
import together_ai_trial.services.pylint_services
import together_ai_trial.services.extract_code_service as code_service

prompts = read_prompts_toml()

async def run_model(model_name, question):
    together.api_key = cfg.together_api_key
    time_start = time.perf_counter()
    output = together.Complete.create(
                    prompt = f"<human>: {question}\n<bot>:", 
                    model =  model_name, 
                    max_tokens = 500,
                    temperature = 0.1,
                    top_k = 50,
                    top_p = 0.6,
                    repetition_penalty = 1.1,
                    stop = ['<human>', '\n\n']
                    )
    logger.info(output["output"])
    time_elapsed = (time.perf_counter() - time_start)
    output_model = output["output"]["choices"][0]["text"]
    return output_model, time_elapsed

async def add_comments(model_name, code, ques):
    together.api_key = cfg.together_api_key
    code_extract = code_service.extract_code(code)
    print(code_extract)
    output = together.Complete.create(
                    prompt = f"""  Can you please add comments to all functions using the reStructuredText Docstring Format for the following code: {code_extract}""", 
                    model =  model_name, 
                    max_tokens = 500,
                    temperature = 0.1,
                    top_k = 50,
                    top_p = 0.6,
                    repetition_penalty = 1.1,
                    stop = ['<human>', '\n\n']
                    )
    output_model = output["output"]["choices"][0]["text"]
    d = datetime.datetime.now()
    date_now = d.date()
    question = ques.replace(" ", "")
    question.strip("\n")
    code_comment = cfg.code_comment
    index = model_name.find('/') #stores the index of a substring or char
    model = model_name[index+1:]
    code_comment_path = pathlib.Path(f"{code_comment}/{date_now}_{ques}")
    if not code_comment_path.exists():
        code_comment_path.mkdir(exist_ok=True, parents=True)
    with open(code_comment_path/f"{model}.txt", mode="w") as f:
        f.write("============")
        f.write('\n')
        f.write(output_model)
        f.write('\n')
        f.write("============")
        f.write('\n')
    return output_model

async def save_to_file(model, output, time_exec, question):
    code_output = pathlib.Path(f"/tmp/togetherai_output")
    if not code_output.exists():
        code_output.mkdir(exist_ok=True, parents=True)
    d = datetime.datetime.now()
    date_now = d.date()
    question_name = question.replace(" ", "")
    question_name = question_name.replace("\n", "")

    with open(code_output/f"{date_now}_{question_name}_together_report.md", mode="a+") as f:
        f.write("\n")
        f.write("=========")
        f.write("\n")
        f.write("# "+ model)
        f.write("\n")
        f.write("## "+ str(date_now))
        f.write("\n")
        f.write(question + "\n" +output)
        f.write("\n")
        f.write(str(time_exec) + "seconds")
        f.write("\n")
        f.write("=========")

async def add_to_df(data):
    

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data)

    # Specify the Excel file path
    excel_file_path = f'{cfg.code_output}\open_source_models.xlsx'

    # Try to read the existing Excel file if it exists
    try:
        existing_df = pd.read_excel(excel_file_path)
        # Append the new data to the existing DataFrame
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame with the data
        pass

    # Write the DataFrame to the Excel file
    df.to_excel(excel_file_path, index=False)
    


async def save_to_excel(df):
    fpath = f'{cfg.code_output}\open_source_models.xlsx'
    import os


    if os.path.exists(fpath):
        with pd.ExcelWriter(fpath, mode='a', engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
    else:
         df.to_excel(fpath, index=False)
    
    
    
if __name__ == "__main__":
    import asyncio
    import together_ai_trial.services.pylint_services as pylint_services

    model ="WizardLM/WizardCoder-15B-V1.0"
    ques = "Generate python code to display numbers from 1 to 30"
    output =  """"
    ```python
for i in range(1, 31):
    print(i)
```

This code uses a for loop and the `range()` function to iterate over the numbers from 1 to 30 (inclusive) and print each number on a new line. 
The `range()` function generates a sequence of numbers starting from the first argument (1) and ending at the second argument (31), incrementing by 1 each time.
    """
    #pylint_file = asyncio.run(pylint_services.lint_code(output, ques, model))
    #f = open(pylint_file, 'r')
    #pylint_output = f.read()
    #df ={"Model": [model], 'Question': [ques], 'Model output': [output], 'Time for execution': 3.5, 'Pylint result': [pylint_output], 'Is the code correct': 'True'}
    #df_new = asyncio.run(add_to_df(df))
    #print(df_new)
    #asyncio.run(save_to_excel(df_new))


    output_comments = asyncio.run(add_comments(model, output))
    print(output_comments)

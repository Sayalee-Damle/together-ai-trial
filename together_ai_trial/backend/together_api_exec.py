import datetime
import pathlib
import time
import together
import pandas as pd
from openpyxl import load_workbook



from together_ai_trial.configuration.config import cfg
from together_ai_trial.configuration.log_factory import logger
import together_ai_trial.services.pylint_services

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

async def save_to_file(model, output, time_exec, question):
    code_output = pathlib.Path(f"/tmp/togetherai_output")
    if not code_output.exists():
        code_output.mkdir(exist_ok=True, parents=True)
    d = datetime.datetime.now()
    date_now = d.date()
    question_name = question.replace(" ", "")
    question_name.strip("\n")
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

async def add_to_df(model, question, output, time_exec, pylint_output, pylint_exec):
    df = pd.DataFrame(index=cfg.model_list, columns=["Model", 'Question', 'Model output', 'Time for execution', 'Pylint result', 'Is the code correct'])
    selected_columns = ["Model",'Question', 'Model output', 'Time for execution', 'Pylint result', 'Is the code correct']
    rows_to_add = [model, question, output, time_exec, pylint_output, pylint_exec]

    dictionary = dict(zip(selected_columns, rows_to_add))
    new_record = pd.DataFrame(dictionary)
        
    df = pd.concat([df, new_record], ignore_index=True)
    return df

    """path = 'open_source_models.xlsx'

   
    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine='openpyxl')
    writer.book = book
    writer.sheets = {ws.title: ws for ws in book.worksheets}

    for sheetname in writer.sheets:
        df.to_excel(writer,sheet_name=sheetname, startrow=writer.sheets[sheetname].max_row, index = False,header= False)

    writer.save()"""
async def save_to_excel(df):
    fpath = 'open_source_models.xlsx'
    with pd.ExcelWriter(fpath, mode="a") as f:
        df.to_excel(f)

    
    
